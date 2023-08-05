#  Copyright 2022 Zurich Instruments AG
#  SPDX-License-Identifier: Apache-2.0

# Copyright 2022 Zurich Instruments AG
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import copy
import logging
import math
import os
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

import numpy as np
from engineering_notation import EngNumber
from sortedcontainers import SortedDict

from laboneq.compiler.code_generator.measurement_calculator import MeasurementCalculator
from laboneq.compiler.event_graph import EventType
from laboneq.compiler.experiment_dao import PulseDef, SectionInfo
from laboneq.compiler.section_graph import SectionGraph
from laboneq.core.exceptions import LabOneQException
from laboneq.core.types.compiled_experiment import (
    PulseInstance,
    PulseMapEntry,
    PulseWaveformMap,
)
from laboneq.core.utilities.pulse_sampler import (
    length_to_samples,
    sample_pulse,
)
from laboneq.compiler.code_generator.analyze_events import (
    analyze_init_times,
    analyze_play_wave_times,
    analyze_set_oscillator_times,
    analyze_loop_times,
    analyze_acquire_times,
    analyze_phase_reset_times,
    analyze_precomp_reset_times,
    phase_int_to_float,
)
from .compressor import compress_generators, compress_generators_rle
from ..awg_info import AWGInfo
from ..awg_signal_type import AWGSignalType
from .signal_obj import SignalObj
from ..trigger_mode import TriggerMode
from .dict_list import merge_dict_list
from .signatures import WaveformSignature
from .utils import normalize_phase
from .wave_index_tracker import WaveIndexTracker
from .command_table_tracker import CommandTableTracker
from .seq_c_generator import SeqCGenerator, string_sanitize
from .seqc_tracker import SeqCTracker
from ..compiler_settings import CompilerSettings
from ..device_type import DeviceType

_logger = logging.getLogger(__name__)


class CodeGenerator:
    USE_ZSYNC_TRIGGER = True

    DELAY_FIRST_AWG = 32 / DeviceType.HDAWG.sampling_rate
    DELAY_OTHER_AWG = 32 / DeviceType.HDAWG.sampling_rate
    DELAY_UHFQA = 140 / DeviceType.HDAWG.sampling_rate

    PHASE_RESOLUTION_BITS = 7

    # This is used as a workaround for the SHFQA requiring that for sampled pulses,  abs(s)  < 1.0 must hold
    # to be able to play pulses with an amplitude of 1.0, we scale complex pulses by this factor
    SHFQA_COMPLEX_SAMPLE_SCALING = 1 - 1e-10

    _measurement_calculator = MeasurementCalculator

    def __init__(self, settings: CompilerSettings = None):
        if settings is not None:
            if isinstance(settings, CompilerSettings):
                self._settings = settings
            else:
                self._settings = CompilerSettings(**settings)
        else:
            self._settings = CompilerSettings()

        self._signals: Dict[str, SignalObj] = {}
        self._code = {}
        self._src = []
        self._wave_indices_all = []
        self._waves = []
        self._command_tables: List[Dict[str, Any]] = []
        self._pulse_map: Dict[str, PulseMapEntry] = {}
        self._sampled_signatures: Dict[str, Dict[WaveformSignature, Dict]] = {}
        self._sampled_events = None
        self._awgs: Dict[CodeGenerator.AwgKey, AWGInfo] = {}
        self._events_in_samples = {}
        self._integration_weights = None
        self._simultaneous_acquires = None
        self._total_execution_time = None

        self.EMIT_TIMING_COMMENTS = self._settings.EMIT_TIMING_COMMENTS

    def integration_weights(self):
        return self._integration_weights

    def simultaneous_acquires(self):
        return self._simultaneous_acquires

    def total_execution_time(self):
        return self._total_execution_time

    @dataclass(init=True, repr=True, order=True, frozen=True)
    class AwgKey:
        device_id: str
        awg_number: int

    def _add_signal_to_awg(self, signal_obj: SignalObj):
        awg_key = CodeGenerator.AwgKey(signal_obj.device_id, signal_obj.awg.awg_number)
        if awg_key not in self._awgs:
            self._awgs[awg_key] = copy.deepcopy(signal_obj.awg)
            self._awgs[awg_key].device_type = signal_obj.device_type
        self._awgs[awg_key].signals.append(signal_obj)

    def add_signal(self, signal: SignalObj):
        signal_obj = copy.deepcopy(signal)
        signal_obj.pulses = []
        _logger.debug(signal_obj)
        self._signals[signal.id] = signal_obj
        self._add_signal_to_awg(signal_obj)

    def sort_signals(self):
        for awg in self._awgs.values():
            awg.signals = list(
                sorted(awg.signals, key=lambda signal: tuple(signal.channels))
            )

    def _append_to_pulse_map(self, signature_pulse_map, sig_string):
        if signature_pulse_map is None:
            return
        for pulse_id, pulse_waveform_map in signature_pulse_map.items():
            pulse_map_entry = self._pulse_map.setdefault(pulse_id, PulseMapEntry())
            pulse_map_entry.waveforms[sig_string] = pulse_waveform_map

    def _save_wave_bin(
        self, samples, signature_pulse_map, sig_string: str, suffix: str
    ):
        filename = sig_string + suffix + ".wave"
        self._waves.append({"filename": filename, "samples": samples})
        self._append_to_pulse_map(signature_pulse_map, sig_string)

    def gen_waves(self):
        if _logger.getEffectiveLevel() == logging.DEBUG:
            _logger.debug("Sampled signatures: %s", self._sampled_signatures)
        for awg in self._awgs.values():
            # Handle integration weights separately
            for signal_obj in awg.signals:
                if signal_obj.id in self._integration_weights:
                    signal_weights = self._integration_weights[signal_obj.id]
                    for weight in signal_weights.values():
                        basename = weight["basename"]
                        if signal_obj.device_type.supports_complex_waves:
                            self._save_wave_bin(
                                CodeGenerator.SHFQA_COMPLEX_SAMPLE_SCALING
                                * (weight["samples_i"] - 1j * weight["samples_q"]),
                                None,
                                basename,
                                "",
                            )
                        else:
                            self._save_wave_bin(
                                weight["samples_i"], None, basename, "_i"
                            )
                            self._save_wave_bin(
                                weight["samples_q"], None, basename, "_q"
                            )

            signals_to_process = awg.signals
            virtual_signal_id = None
            if awg.signal_type == AWGSignalType.MULTI:
                iq_signal_ids = []
                signals_to_process = []
                for signal_obj in awg.signals:
                    if signal_obj.signal_type != "integration":
                        _logger.debug(
                            "Non-integration signal in multi signal: %s", signal_obj
                        )
                        iq_signal_ids.append(signal_obj.id)
                    else:
                        signals_to_process.append(signal_obj)
                virtual_signal_id = "_".join(iq_signal_ids)
            elif awg.signal_type == AWGSignalType.DOUBLE:
                virtual_signal_id = (
                    signals_to_process[0].id + "_" + signals_to_process[1].id
                )

            if virtual_signal_id is None:
                for signal_obj in signals_to_process:
                    if signal_obj.id in self._sampled_signatures:
                        for (
                            signature_key,
                            sampled_signature,
                        ) in self._sampled_signatures[signal_obj.id].items():
                            sig_string, _ = signature_key.signature_string()
                            if signal_obj.device_type.supports_binary_waves:
                                if awg.signal_type == AWGSignalType.SINGLE:
                                    self._save_wave_bin(
                                        sampled_signature["samples_i"],
                                        sampled_signature["signature_pulse_map"],
                                        sig_string,
                                        "",
                                    )
                                else:
                                    self._save_wave_bin(
                                        sampled_signature["samples_i"],
                                        sampled_signature["signature_pulse_map"],
                                        sig_string,
                                        "_i",
                                    )
                                    if "samples_q" in sampled_signature:
                                        self._save_wave_bin(
                                            sampled_signature["samples_q"],
                                            sampled_signature["signature_pulse_map"],
                                            sig_string,
                                            "_q",
                                        )
                            elif signal_obj.device_type.supports_complex_waves:
                                self._save_wave_bin(
                                    CodeGenerator.SHFQA_COMPLEX_SAMPLE_SCALING
                                    * (
                                        sampled_signature["samples_i"]
                                        - 1j * sampled_signature["samples_q"]
                                    ),
                                    sampled_signature["signature_pulse_map"],
                                    sig_string,
                                    "",
                                )
                            else:
                                raise RuntimeError(
                                    f"Device type {signal_obj.device_type} has invalid supported waves config."
                                )
            else:
                signal_obj = awg.signals[0]
                for signature_key, sampled_signature in self._sampled_signatures[
                    virtual_signal_id
                ].items():
                    sig_string, _ = signature_key.signature_string()
                    if signal_obj.device_type.supports_binary_waves:
                        self._save_wave_bin(
                            sampled_signature["samples_i"],
                            sampled_signature["signature_pulse_map"],
                            sig_string,
                            "_i",
                        )
                        if "samples_q" in sampled_signature:
                            self._save_wave_bin(
                                sampled_signature["samples_q"],
                                sampled_signature["signature_pulse_map"],
                                sig_string,
                                "_q",
                            )
                    else:
                        raise RuntimeError(
                            f"Device type {signal_obj.device_type} has invalid supported waves config."
                        )

        if _logger.getEffectiveLevel() == logging.DEBUG:
            _logger.debug("Sampled signatures: %s", self._sampled_signatures)

            _logger.debug(self._waves)

    def gen_acquire_map(self, events: List[Any], sections: SectionGraph):
        # todo (PW): this can EASILY be factored out into a separate file
        loop_events = [
            e
            for e in events
            if e["event_type"] == "LOOP_ITERATION_END" and not e.get("shadow")
        ]
        averaging_loop_info: SectionInfo = None
        innermost_loop: Dict[str, Any] = None
        outermost_loop: Dict[str, Any] = None
        for e in loop_events:
            section_info = sections.section_info(e["section_name"])
            if section_info.averaging_type == "hardware":
                averaging_loop_info = section_info
            if (
                innermost_loop is None
                or e["nesting_level"] > innermost_loop["nesting_level"]
            ):
                innermost_loop = e
            if (
                outermost_loop is None
                or e["nesting_level"] < outermost_loop["nesting_level"]
            ):
                outermost_loop = e
        averaging_loop = (
            None
            if averaging_loop_info is None
            else innermost_loop
            if averaging_loop_info.averaging_mode == "sequential"
            else outermost_loop
        )
        if (
            averaging_loop is not None
            and averaging_loop["section_name"] != averaging_loop_info.section_id
        ):
            raise RuntimeError(
                f"Internal error: couldn't unambiguously determine the hardware averaging loop - "
                f"innermost '{innermost_loop['section_name']}', outermost '{outermost_loop['section_name']}', "
                f"hw avg '{averaging_loop_info.section_id}' with mode '{averaging_loop_info.averaging_mode}' "
                f"expected to match '{averaging_loop['section_name']}'"
            )
        unrolled_avg_matcher = re.compile(
            "(?!)"  # Never match anything
            if averaging_loop is None
            else f"{averaging_loop['section_name']}_[0-9]+"
        )
        # timestamp -> map[signal -> handle]
        self._simultaneous_acquires: Dict[float, Dict[str, str]] = {}
        for e in events:
            if (
                e["event_type"] == "ACQUIRE_START"
                # Skip injected spectroscopy events (obsolete hack)
                and e["acquisition_type"] != ["spectroscopy"]
            ):
                if e.get("shadow") and unrolled_avg_matcher.match(
                    e.get("loop_iteration")
                ):
                    continue  # Skip events for unrolled averaging loop
                time_events = self._simultaneous_acquires.setdefault(e["time"], {})
                time_events[e["signal"]] = e["acquire_handle"]

    def gen_seq_c(self, events: List[Any], pulse_defs: Dict[str, PulseDef]):
        signal_keys = [
            "sampling_rate",
            "id",
            "device_id",
            "device_type",
            "delay_signal",
        ]
        signal_info_map = {
            id: {k: getattr(s, k) for k in signal_keys}
            for id, s in self._signals.items()
        }
        for k, s in signal_info_map.items():
            s["awg_number"] = self._signals[k].awg.awg_number

        (
            integration_times,
            signal_delays,
            delays_per_awg,
        ) = self._measurement_calculator.calculate_integration_times(
            signal_info_map, events
        )

        for signal_id, signal_obj in self._signals.items():
            code_generation_delay = signal_delays.get(signal_id)
            if code_generation_delay is not None:

                signal_obj.total_delay = (
                    signal_obj.start_delay
                    + signal_obj.delay_signal
                    + code_generation_delay["code_generation"]
                )
                signal_obj.on_device_delay = code_generation_delay["on_device"]
            else:
                signal_obj.total_delay = (
                    signal_obj.start_delay + signal_obj.delay_signal
                )

            _logger.debug(
                "Processed signal obj %s signal_obj.start_delay=%s  signal_obj.delay_signal=%s signal_obj.total_delay=%s  signal_obj.on_device_delay=%s",
                signal_id,
                EngNumber(signal_obj.start_delay),
                EngNumber(signal_obj.delay_signal),
                EngNumber(signal_obj.total_delay),
                EngNumber(signal_obj.on_device_delay),
            )

        self._total_execution_time = events[-1].get("time") if len(events) > 0 else None
        self.sort_signals()
        self._integration_weights = {}

        ignore_pulses = set()
        for pulse_id, pulse_def in pulse_defs.items():
            if (
                abs(pulse_def.effective_amplitude) < 1e-12
            ):  # ignore zero amplitude pulses
                ignore_pulses.add(pulse_id)
        if len(ignore_pulses) > 0:
            _logger.debug(
                "Ignoring pulses because of zero amplitude: %s", ignore_pulses
            )

        filtered_events: List[Any] = [
            event
            for event in events
            if "play_wave_id" not in event or event["play_wave_id"] not in ignore_pulses
        ]

        for _, awg in sorted(
            self._awgs.items(),
            key=lambda item: item[0].device_id + str(item[0].awg_number),
        ):
            self._gen_seq_c_per_awg(awg, filtered_events, pulse_defs)

        return integration_times, signal_delays

    @staticmethod
    def _calc_global_awg_params(awg: AWGInfo) -> Tuple[float, float]:
        global_sampling_rate = None
        global_delay = None
        signals_so_far = set()
        all_total_delays = set()
        all_start_delays = set()
        all_delay_signals = set()
        all_relevant_delays = {}
        for signal_obj in awg.signals:

            _logger.debug(f"considering signal {signal_obj.id}")
            if awg.device_type == DeviceType.UHFQA:
                # on the UHFQA, we allow an individual delay_signal on the measure (play) line, even though we can't
                # shift the play time with a node on the device
                # for this to work, we need to ignore the play delay when generating code for loop events
                # and we use the start delay (lead time) to calculate the global delay
                relevant_delay = signal_obj.start_delay
            else:
                relevant_delay = signal_obj.total_delay

            if (
                round(relevant_delay * signal_obj.sampling_rate)
                % signal_obj.device_type.sample_multiple
                != 0
            ):
                raise RuntimeError(
                    f"Delay {relevant_delay} s = {round(relevant_delay*signal_obj.sampling_rate)} samples on signal {signal_obj.id} is not compatible with the sample multiple of {signal_obj.device_type.sample_multiple} on {signal_obj.device_type}"
                )
            all_total_delays.add(signal_obj.total_delay)
            all_start_delays.add(relevant_delay)
            all_delay_signals.add(signal_obj.delay_signal)
            all_relevant_delays[signal_obj.id] = relevant_delay

            if signal_obj.signal_type != "integration":

                if awg.signal_type != AWGSignalType.IQ and global_delay is not None:
                    if global_delay != relevant_delay:
                        raise RuntimeError(
                            f"Delay {relevant_delay * 1e9:.2f} ns on signal "
                            f"{signal_obj.id} is different from other delays "
                            f"({global_delay * 1e9:.2f} ns) on the same AWG, on signals {signals_so_far}"
                        )
                if global_delay is not None:

                    if relevant_delay < global_delay:
                        # use minimum delay as global delay
                        # this makes sure that loop start events happen first and are not shifted beyond loop body events
                        global_delay = relevant_delay
                else:
                    global_delay = relevant_delay

            global_sampling_rate = signal_obj.sampling_rate
            signals_so_far.add(signal_obj.id)

        if global_delay is None:
            global_delay = 0

        if (
            global_delay > 0
            and global_delay
            < awg.device_type.min_play_wave / awg.device_type.sampling_rate
        ):
            global_delay = 0

        _logger.debug(
            "Global delay for %s awg %s: %ss, calculated from all_relevant_delays %s",
            awg.device_id,
            awg.awg_number,
            EngNumber(global_delay or 0),
            [(s, EngNumber(d)) for s, d in all_relevant_delays.items()],
        )

        return global_sampling_rate, global_delay

    def _gen_seq_c_per_awg(
        self, awg: AWGInfo, events: List[Any], pulse_defs: Dict[str, PulseDef]
    ):
        wave_indices = WaveIndexTracker()
        declarations_generator = SeqCGenerator()
        declared_variables = set()
        _logger.debug("Generating seqc for awg %d of %s", awg.awg_number, awg.device_id)
        _logger.debug("AWG Object = \n%s", awg)
        sampled_events = SortedDict()
        filename = awg.seqc

        global_sampling_rate, global_delay = self._calc_global_awg_params(awg)
        if self.EMIT_TIMING_COMMENTS:
            declarations_generator.add_comment(
                f"{awg.seqc} global delay {EngNumber(global_delay)} sampling_rate: {EngNumber(global_sampling_rate)}Sa/s "
            )

        use_command_table = (
            awg.device_type == DeviceType.HDAWG
            and self._settings.HDAWG_FORCE_COMMAND_TABLE
        ) or (
            awg.device_type == DeviceType.SHFSG
            and self._settings.SHFSG_FORCE_COMMAND_TABLE
        )
        command_table_tracker = CommandTableTracker()

        signal_ids = set(signal.id for signal in awg.signals)
        own_sections = set(
            event["section_name"]
            for event in events
            if event.get("signal") in signal_ids
            or event["event_type"]
            in (
                EventType.PARAMETER_SET,
                EventType.RESET_SW_OSCILLATOR_PHASE,
                EventType.INCREMENT_OSCILLATOR_PHASE,
                EventType.SET_OSCILLATOR_FREQUENCY_START,
            )
        )
        for event in events:
            if (
                event["event_type"] == EventType.SUBSECTION_END
                and event["subsection_name"] in own_sections
            ):
                # by looking at SUBSECTION_END, we'll always walk towards the tree root
                own_sections.add(event["section_name"])

        # filter the event list
        events = [
            event
            for event in events
            if "section_name" not in event or event.get("section_name") in own_sections
        ]

        _logger.debug(
            "Analyzing initialization events for awg %d of %s",
            awg.awg_number,
            awg.device_id,
        )
        init_events = analyze_init_times(
            awg.device_id, global_sampling_rate, global_delay
        )
        merge_dict_list(sampled_events, init_events)

        precomp_reset_events = analyze_precomp_reset_times(
            events, awg.device_id, global_sampling_rate, global_delay
        )
        merge_dict_list(sampled_events, precomp_reset_events)

        phase_reset_events = analyze_phase_reset_times(
            events, awg.device_id, global_sampling_rate, global_delay
        )
        merge_dict_list(sampled_events, phase_reset_events)

        loop_events = analyze_loop_times(
            awg, events, global_sampling_rate, global_delay
        )
        merge_dict_list(sampled_events, loop_events)

        for signal_obj in awg.signals:

            set_oscillator_events = analyze_set_oscillator_times(
                events,
                signal_obj.id,
                device_id=signal_obj.device_id,
                device_type=signal_obj.device_type,
                sampling_rate=signal_obj.sampling_rate,
                delay=signal_obj.total_delay,
            )
            merge_dict_list(sampled_events, set_oscillator_events)

            acquire_events = analyze_acquire_times(
                events,
                signal_obj.id,
                sampling_rate=signal_obj.sampling_rate,
                delay=signal_obj.total_delay,
                sample_multiple=signal_obj.device_type.sample_multiple,
                channels=signal_obj.channels,
            )

            if signal_obj.signal_type == "integration":
                _logger.debug(
                    "Calculating integration weights for signal %s. There are %d acquire events.",
                    signal_obj.id,
                    len(acquire_events.values()),
                )
                integration_weights = {}
                for event_list in acquire_events.values():
                    for event in event_list:
                        _logger.debug("For weights, look at %s", event)
                        if "play_wave_id" in event:
                            play_wave_id = event["play_wave_id"]
                            _logger.debug(
                                "Event %s has play wave id %s", event, play_wave_id
                            )
                            if (
                                play_wave_id in pulse_defs
                                and play_wave_id not in integration_weights
                            ):
                                pulse_def = pulse_defs[play_wave_id]
                                _logger.debug("Pulse def: %s", pulse_def)

                                if None is pulse_def.samples is pulse_def.function:
                                    # Not a real pulse, just a placeholder for the length - skip
                                    continue

                                samples = pulse_def.samples
                                amplitude = pulse_def.effective_amplitude

                                if samples is None:
                                    amplitude = amplitude * math.sqrt(2)

                                length = pulse_def.length
                                if length is None:
                                    length = len(samples) / signal_obj.sampling_rate

                                _logger.debug(
                                    "Sampling integration weights for %s with modulation_frequency %s",
                                    signal_obj.id,
                                    str(signal_obj.oscillator_frequency),
                                )
                                complex_modulation = awg.device_type != DeviceType.UHFQA

                                integration_weight = sample_pulse(
                                    signal_type="iq",
                                    sampling_rate=signal_obj.sampling_rate,
                                    length=length,
                                    amplitude=amplitude,
                                    pulse_function=pulse_def.function,
                                    modulation_frequency=signal_obj.oscillator_frequency,
                                    iq_phase=signal_obj.device_type.iq_phase,
                                    samples=samples,
                                    complex_modulation=complex_modulation,
                                    pulse_parameters=event.get("pulse_parameters"),
                                )

                                integration_weight["basename"] = (
                                    signal_obj.device_id
                                    + "_"
                                    + str(signal_obj.awg.awg_number)
                                    + "_"
                                    + str(min(signal_obj.channels))
                                    + "_"
                                    + play_wave_id
                                )
                                integration_weights[play_wave_id] = integration_weight

                self._integration_weights[signal_obj.id] = integration_weights

            merge_dict_list(sampled_events, acquire_events)

        signals_to_process = awg.signals
        oscillator_frequencies_per_channel = []
        if awg.signal_type == AWGSignalType.MULTI:
            _logger.debug("Multi signal %s", awg)
            iq_signal_ids = []
            signals_to_process = []
            iq_signals = []
            delay = None
            for signal_obj in awg.signals:
                if signal_obj.signal_type != "integration":
                    _logger.debug(
                        "Non-integration signal in multi signal: %s", signal_obj
                    )
                    iq_signal_ids.append(signal_obj.id)
                    oscillator_frequencies_per_channel.append(
                        signal_obj.oscillator_frequency
                    )
                    iq_signals.append(signal_obj)
                    delay = signal_obj.total_delay
                else:
                    signals_to_process.append(signal_obj)

            virtual_signal_id = "_".join(iq_signal_ids)
            iq_phase = iq_signals[0].device_type.iq_phase

            interval_events = analyze_play_wave_times(
                events=events,
                signals=self._signals,
                signal_ids=iq_signal_ids,
                device_type=signal_obj.device_type,
                sampling_rate=signal_obj.sampling_rate,
                delay=delay,
                other_events=sampled_events,
                iq_phase=iq_phase,
                phase_resolution_range=self.phase_resolution_range(),
                waveform_size_hints=self.waveform_size_hints(signal_obj.device_type),
            )

            sampled_signatures = self._sample_pulses(
                virtual_signal_id,
                interval_events,
                pulse_defs=pulse_defs,
                sampling_rate=signal_obj.sampling_rate,
                signal_type="iq",
                device_type=signal_obj.device_type,
                oscillator_frequency=None,
                oscillator_frequencies_per_channel=oscillator_frequencies_per_channel,
                multi_iq_signal=True,
            )

            self._sampled_signatures[virtual_signal_id] = sampled_signatures
            merge_dict_list(sampled_events, interval_events)
            if virtual_signal_id in self._sampled_signatures:
                for sig in self._sampled_signatures[virtual_signal_id].keys():
                    sig_string, long_sig = sig.signature_string()
                    if long_sig is not None:
                        declarations_generator.add_comment(
                            f"{sig_string} is {long_sig}"
                        )
                    length = sig.length
                    declarations_generator.add_wave_declaration(
                        signal_obj.device_type,
                        awg.signal_type.value,
                        sig_string,
                        length,
                    )

        if awg.signal_type != AWGSignalType.DOUBLE:
            for signal_obj in signals_to_process:

                iq_phase = signal_obj.device_type.iq_phase
                if signal_obj.device_type == DeviceType.SHFQA:
                    sub_channel = signal_obj.channels[0]
                else:
                    sub_channel = None
                interval_events = analyze_play_wave_times(
                    events=events,
                    signals=self._signals,
                    signal_ids=[signal_obj.id],
                    device_type=signal_obj.device_type,
                    sampling_rate=signal_obj.sampling_rate,
                    delay=signal_obj.total_delay,
                    other_events=sampled_events,
                    iq_phase=iq_phase,
                    phase_resolution_range=self.phase_resolution_range(),
                    waveform_size_hints=self.waveform_size_hints(
                        signal_obj.device_type
                    ),
                    sub_channel=sub_channel,
                )

                sampled_signatures = self._sample_pulses(
                    signal_obj.id,
                    interval_events,
                    pulse_defs=pulse_defs,
                    sampling_rate=signal_obj.sampling_rate,
                    signal_type=signal_obj.signal_type,
                    device_type=signal_obj.device_type,
                    oscillator_frequency=signal_obj.oscillator_frequency,
                )

                self._sampled_signatures[signal_obj.id] = sampled_signatures
                merge_dict_list(sampled_events, interval_events)

                if signal_obj.id in self._sampled_signatures:
                    signature_infos = []
                    for sig in self._sampled_signatures[signal_obj.id].keys():
                        sig_string, _ = sig.signature_string()
                        length = sig.length
                        signature_infos.append((sig_string, length))

                    for siginfo in sorted(signature_infos):
                        declarations_generator.add_wave_declaration(
                            signal_obj.device_type,
                            signal_obj.signal_type,
                            siginfo[0],
                            siginfo[1],
                        )
        else:
            virtual_signal_id = (
                signals_to_process[0].id + "_" + signals_to_process[1].id
            )
            interval_events = analyze_play_wave_times(
                events=events,
                signals=self._signals,
                signal_ids=[
                    signals_to_process[0].id,
                    signals_to_process[1].id,
                ],
                device_type=signal_obj.device_type,
                sampling_rate=signal_obj.sampling_rate,
                delay=signal_obj.total_delay,
                other_events=sampled_events,
                iq_phase=0,
                phase_resolution_range=self.phase_resolution_range(),
                waveform_size_hints=self.waveform_size_hints(signal_obj.device_type),
            )

            sampled_signatures = self._sample_pulses(
                virtual_signal_id,
                interval_events,
                pulse_defs=pulse_defs,
                sampling_rate=signals_to_process[0].sampling_rate,
                signal_type=signals_to_process[0].signal_type,
                device_type=signals_to_process[0].device_type,
                oscillator_frequency=None,
                oscillator_frequencies_per_channel=[
                    signals_to_process[0].oscillator_frequency,
                    signals_to_process[1].oscillator_frequency,
                ],
            )

            self._sampled_signatures[virtual_signal_id] = sampled_signatures
            merge_dict_list(sampled_events, interval_events)
            if virtual_signal_id in self._sampled_signatures:
                for sig in self._sampled_signatures[virtual_signal_id].keys():
                    sig_string, _ = sig.signature_string()
                    length = sig.length
                    declarations_generator.add_wave_declaration(
                        signals_to_process[0].device_type,
                        awg.signal_type.value,
                        sig_string,
                        length,
                    )
        self._sampled_events = sampled_events
        self.post_process_sampled_events(awg, sampled_events)

        seqc_tracker = None
        deferred_function_calls = []
        init_generator = SeqCGenerator()
        if signal_obj.trigger_mode == TriggerMode.DIO_TRIGGER:
            if awg.awg_number == 0:
                init_generator.add_function_call_statement("setDIO", ["0"])
                init_generator.add_function_call_statement("wait", ["2000000"])
                init_generator.add_function_call_statement("playZero", ["512"])
                if signal_obj.reference_clock_source != "internal":
                    init_generator.add_function_call_statement("waitDigTrigger", ["1"])
                init_generator.add_function_call_statement("setDIO", ["0xffffffff"])
                init_generator.add_function_call_statement("waitDIOTrigger")
                delay_first_awg_samples = str(
                    round(signal_obj.sampling_rate * CodeGenerator.DELAY_FIRST_AWG / 16)
                    * 16
                )
                if int(delay_first_awg_samples) > 0:
                    deferred_function_calls.append(
                        {"name": "playZero", "args": [delay_first_awg_samples]}
                    )
                    deferred_function_calls.append({"name": "waitWave", "args": []})
            else:
                init_generator.add_function_call_statement("waitDIOTrigger")
                delay_other_awg_samples = str(
                    round(signal_obj.sampling_rate * CodeGenerator.DELAY_OTHER_AWG / 16)
                    * 16
                )
                if int(delay_other_awg_samples) > 0:
                    deferred_function_calls.append(
                        {"name": "playZero", "args": [delay_other_awg_samples]}
                    )
                    deferred_function_calls.append({"name": "waitWave", "args": []})

        elif signal_obj.trigger_mode == TriggerMode.DIO_WAIT:
            init_generator.add_variable_declaration("dio", "0xffffffff")
            body = SeqCGenerator()
            body.add_function_call_statement("getDIO", args=None, assign_to="dio")
            init_generator.add_do_while("dio & 0x0001", body)
            init_generator.add_function_call_statement("waitDIOTrigger")
            delay_uhfqa_samples = str(
                round(signal_obj.sampling_rate * CodeGenerator.DELAY_UHFQA / 8) * 8
            )
            if int(delay_uhfqa_samples) > 0:
                init_generator.add_function_call_statement(
                    "playZero", [delay_uhfqa_samples]
                )
                init_generator.add_function_call_statement("waitWave")

        elif signal_obj.trigger_mode == TriggerMode.INTERNAL_TRIGGER_WAIT:
            init_generator.add_function_call_statement("waitDigTrigger", ["1"])

        else:
            if (
                CodeGenerator.USE_ZSYNC_TRIGGER
                and signal_obj.device_type.supports_zsync
            ):
                init_generator.add_function_call_statement("waitZSyncTrigger")
            else:
                init_generator.add_function_call_statement("waitDIOTrigger")

        _logger.debug(
            "** Start processing events for awg %d of %s",
            awg.awg_number,
            awg.device_id,
        )
        loop_stack = []

        seqc_tracker = SeqCTracker(
            init_generator=init_generator,
            deferred_function_calls=seqc_tracker.deferred_function_calls
            if seqc_tracker is not None
            else deferred_function_calls,
            sampling_rate=global_sampling_rate,
            delay=global_delay,
            device_type=signal_obj.device_type,
            emit_timing_comments=self.EMIT_TIMING_COMMENTS,
            logger=_logger,
        )

        last_event = None

        for sampled_event_list in sampled_events.values():
            _logger.debug("EventListBeforeSort: %s", sampled_event_list)
            sampled_event_list = CodeGenerator.sort_events(sampled_event_list)
            _logger.debug("-Processing list:")
            for sampled_event_for_log in sampled_event_list:
                _logger.debug("       %s", sampled_event_for_log)
            _logger.debug("-End event list")

            for sampled_event in sampled_event_list:
                _logger.debug("  Processing event %s", sampled_event)

                signature = sampled_event["signature"]
                start = sampled_event["start"]
                if signature == "playwave":
                    signature = sampled_event["playback_signature"]
                    signal_id = sampled_event["signal_id"]

                    if signature.hw_oscillator is not None and not use_command_table:
                        raise LabOneQException(
                            "HW oscillator switching only possible in experimental "
                            "command-table mode"
                        )

                    if (
                        signal_id not in self._sampled_signatures
                        or signature.waveform not in self._sampled_signatures[signal_id]
                    ):
                        _logger.debug(
                            "  Found no matching signature for event %s",
                            signature,
                            sampled_event,
                        )
                        continue

                    _logger.debug(
                        "  Found matching signature %s for event %s",
                        signature,
                        sampled_event,
                    )
                    seqc_tracker.add_required_playzeros(sampled_event)
                    seqc_tracker.add_timing_comment(sampled_event["end"])
                    generator = seqc_tracker.current_loop_stack_generator()

                    play_wave_channel = None
                    if len(signal_obj.channels) > 0:
                        play_wave_channel = signal_obj.channels[0] % 2

                    signal_type_for_wave_index = (
                        awg.signal_type.value
                        if signal_obj.device_type.supports_binary_waves
                        else "csv"
                        # Include CSV waves into the index to keep track of waves-AWG mapping
                    )
                    sig_string, _ = signature.waveform.signature_string()
                    wave_index = wave_indices.lookup_index_by_wave_id(sig_string)
                    if wave_index is None:
                        wave_index = wave_indices.create_index_for_wave(
                            sig_string, signal_type_for_wave_index
                        )
                        if wave_index is not None:
                            generator.add_assign_wave_index_statement(
                                signal_obj.device_type,
                                awg.signal_type.value,
                                sig_string,
                                wave_index,
                                play_wave_channel,
                            )
                    if use_command_table:
                        ct_index = command_table_tracker.lookup_index_by_signature(
                            signature
                        )
                        if ct_index is None:
                            ct_index = command_table_tracker.create_entry(
                                signature, wave_index
                            )
                        comment = sig_string
                        if signature.hw_oscillator is not None:
                            comment += f", osc={signature.hw_oscillator}"
                        generator.add_command_table_execution(ct_index, comment)
                    else:
                        generator.add_play_wave_statement(
                            signal_obj.device_type,
                            awg.signal_type.value,
                            sig_string,
                            play_wave_channel,
                        )
                    seqc_tracker.clear_deferred_function_calls(sampled_event)

                    seqc_tracker.current_time = sampled_event["end"]

                elif signature == "acquire":
                    _logger.debug("  Processing ACQUIRE EVENT %s", sampled_event)

                    args = [
                        "QA_INT_ALL",
                        "1" if "RAW" in sampled_event["acquisition_type"] else "0",
                    ]

                    if start > seqc_tracker.current_time:
                        seqc_tracker.add_required_playzeros(sampled_event)

                        _logger.debug("  Deferring function call for %s", sampled_event)
                        seqc_tracker.add_function_call_statement(
                            name="startQA", args=args, deferred=True
                        )
                    else:
                        skip = False
                        if last_event is not None:
                            if (
                                last_event["signature"] == "acquire"
                                and last_event["start"] == start
                            ):
                                skip = True
                                _logger.debug(
                                    "Skipping acquire event %s because last event was also acquire: %s",
                                    sampled_event,
                                    last_event,
                                )
                        if not skip:
                            seqc_tracker.add_function_call_statement(
                                "startQA", args, deferred=False
                            )

                elif signature == "QA_EVENT":
                    _logger.debug("  Processing QA_EVENT %s", sampled_event)
                    generator_channels = set()
                    for play_event in sampled_event["play_events"]:
                        _logger.debug("  play_event %s", play_event)
                        play_signature = play_event["playback_signature"].waveform
                        if "signal_id" in play_event:
                            signal_id = play_event["signal_id"]
                            if play_signature in self._sampled_signatures[signal_id]:
                                _logger.debug(
                                    "  Found matching signature %s for event %s",
                                    play_signature,
                                    play_event,
                                )
                                current_signal_obj = next(
                                    signal_obj
                                    for signal_obj in awg.signals
                                    if signal_obj.id == signal_id
                                )
                                generator_channels.update(current_signal_obj.channels)
                                (
                                    sig_string,
                                    _,
                                ) = play_signature.signature_string()

                                wave_indices.add_numbered_wave(
                                    sig_string,
                                    "complex",
                                    current_signal_obj.channels[0],
                                )

                    integration_channels = [
                        event["channels"] for event in sampled_event["acquire_events"]
                    ]

                    integration_channels = [
                        item for sublist in integration_channels for item in sublist
                    ]

                    if len(integration_channels) > 0:

                        integrator_mask = "|".join(
                            map(lambda x: "QA_INT_" + str(x), integration_channels)
                        )
                    else:
                        integrator_mask = "QA_INT_NONE"

                    if len(generator_channels) > 0:
                        generator_mask = "|".join(
                            map(lambda x: "QA_GEN_" + str(x), generator_channels)
                        )
                    else:
                        generator_mask = "QA_GEN_NONE"

                    if "spectroscopy" in sampled_event["acquisition_type"]:
                        args = [0, 0, 0, 0, 1]
                    else:
                        args = [
                            generator_mask,
                            integrator_mask,
                            "1" if "RAW" in sampled_event["acquisition_type"] else "0",
                        ]

                    seqc_tracker.add_required_playzeros(sampled_event)

                    if sampled_event["end"] > seqc_tracker.current_time:
                        play_zero_after_qa = (
                            sampled_event["end"] - seqc_tracker.current_time
                        )
                        seqc_tracker.add_timing_comment(sampled_event["end"])
                        seqc_tracker.add_play_zero_statement(
                            play_zero_after_qa, signal_obj.device_type
                        )
                    seqc_tracker.current_time = sampled_event["end"]

                    seqc_tracker.add_function_call_statement("startQA", args)
                    if "spectroscopy" in sampled_event["acquisition_type"]:
                        seqc_tracker.add_function_call_statement("setTrigger", [0])

                elif signature == "reset_precompensation_filters":
                    try:
                        if sampled_event["signal_id"] in (s.id for s in awg.signals):
                            _logger.debug(
                                "  Processing RESET PRECOMPENSATION FILTERS event %s",
                                sampled_event,
                            )
                            seqc_tracker.add_required_playzeros(sampled_event)
                            seqc_tracker.add_function_call_statement(
                                name="setPrecompClear", args=[1]
                            )
                    except KeyError:
                        pass

                elif signature in ("initial_reset_phase", "reset_phase"):
                    # If multiple phase reset events are scheduled at the same time,
                    # only process the *last* one. This way, `reset_phase` takes
                    # precedence.
                    # TODO (PW): Remove this check, once we no longer force oscillator
                    # resets at the start of the sequence.
                    last_reset = [
                        event
                        for event in sampled_event_list
                        if event["signature"] in ("reset_phase", "initial_reset_phase")
                    ][-1]
                    if last_reset is not sampled_event:
                        continue

                    _logger.debug("  Processing RESET PHASE event %s", sampled_event)
                    if signature == "initial_reset_phase":
                        if start > seqc_tracker.current_time:
                            seqc_tracker.add_required_playzeros(sampled_event)
                            if awg.device_type.supports_reset_osc_phase:
                                seqc_tracker.add_function_call_statement(
                                    "resetOscPhase", deferred=True
                                )
                        else:
                            if awg.device_type.supports_reset_osc_phase:
                                seqc_tracker.add_function_call_statement(
                                    "resetOscPhase", deferred=False
                                )
                    elif (
                        signature == "reset_phase"
                        and awg.device_type.supports_reset_osc_phase
                    ):
                        seqc_tracker.add_required_playzeros(sampled_event)
                        seqc_tracker.add_function_call_statement(
                            "resetOscPhase", deferred=True
                        )

                elif signature == "set_oscillator_frequency":
                    iteration = sampled_event["iteration"]
                    parameter_name = sampled_event["parameter_name"]
                    counter_variable_name = string_sanitize(f"index_{parameter_name}")
                    if iteration == 0:
                        if counter_variable_name != f"index_{parameter_name}":
                            _logger.warning(
                                "Parameter name '%s' has been sanitized in generated code.",
                                parameter_name,
                            )
                        declarations_generator.add_variable_declaration(
                            counter_variable_name, 0
                        )
                        declarations_generator.add_function_call_statement(
                            "configFreqSweep",
                            (
                                0,
                                sampled_event["start_frequency"],
                                sampled_event["step_frequency"],
                            ),
                        )
                        seqc_tracker.add_variable_assignment(counter_variable_name, 0)
                    seqc_tracker.add_required_playzeros(sampled_event)
                    seqc_tracker.add_function_call_statement(
                        "setSweepStep",
                        args=(0, f"{counter_variable_name}++"),
                        deferred=True,
                    )

                elif signature == "LOOP_STEP_START":
                    _logger.debug(
                        "  Processing LOOP_STEP_START EVENT %s", sampled_event
                    )
                    seqc_tracker.add_required_playzeros(sampled_event)
                    seqc_tracker.clear_deferred_function_calls(sampled_event)
                    seqc_tracker.append_loop_stack_generator()

                elif signature == "PUSH_LOOP":
                    _logger.debug(
                        "  Processing PUSH_LOOP EVENT %s, top of stack is %s",
                        sampled_event,
                        seqc_tracker.current_loop_stack_generator(),
                    )
                    seqc_tracker.add_required_playzeros(sampled_event)
                    seqc_tracker.clear_deferred_function_calls(sampled_event)
                    seqc_tracker.append_loop_stack_generator(outer=True)

                    if self.EMIT_TIMING_COMMENTS:
                        seqc_tracker.add_comment(
                            f"PUSH LOOP {sampled_event} current time = {seqc_tracker.current_time}"
                        )

                    loop_stack.append(sampled_event)

                elif signature == "ITERATE":
                    if (
                        seqc_tracker.current_loop_stack_generator().num_noncomment_statements()
                        > 0
                    ):
                        _logger.debug(
                            "  Processing ITERATE EVENT %s, loop stack is %s",
                            sampled_event,
                            loop_stack,
                        )
                        if self.EMIT_TIMING_COMMENTS:
                            seqc_tracker.add_comment(
                                f"ITERATE  {sampled_event}, current time = {seqc_tracker.current_time}"
                            )
                        seqc_tracker.add_required_playzeros(sampled_event)
                        seqc_tracker.clear_deferred_function_calls(sampled_event)
                        variable_name = string_sanitize(
                            "repeat_count_" + str(sampled_event["loop_id"])
                        )
                        if variable_name not in declared_variables:
                            declarations_generator.add_variable_declaration(
                                variable_name
                            )
                            declared_variables.add(variable_name)

                        loop_generator = SeqCGenerator()
                        open_generators = seqc_tracker.pop_loop_stack_generators()
                        _logger.debug(
                            "  Popped %s, stack is now %s",
                            open_generators,
                            seqc_tracker.loop_stack_generators,
                        )
                        loop_body = compress_generators(
                            open_generators, declarations_generator
                        )
                        loop_generator.add_countdown_loop(
                            variable_name, sampled_event["num_repeats"], loop_body
                        )
                        if self.EMIT_TIMING_COMMENTS:
                            loop_generator.add_comment(f"Loop for {sampled_event}")
                        start_loop_event = loop_stack.pop()
                        delta = start - start_loop_event["start"]
                        seqc_tracker.current_time = (
                            start_loop_event["start"]
                            + sampled_event["num_repeats"] * delta
                        )
                        if self.EMIT_TIMING_COMMENTS:
                            loop_generator.add_comment(
                                f"Delta: {delta} current time after loop: {seqc_tracker.current_time}, corresponding start event: {start_loop_event}"
                            )
                        seqc_tracker.append_loop_stack_generator(
                            always=True, generator=loop_generator
                        )
                        seqc_tracker.append_loop_stack_generator(always=True)
                    else:
                        seqc_tracker.pop_loop_stack_generators()
                        loop_stack.pop()
                last_event = sampled_event

        seqc_tracker.clear_deferred_function_calls(None)
        seq_c_generators = []
        _logger.debug(
            "***  Finished event processing, loop_stack_generators: %s",
            seqc_tracker.loop_stack_generators,
        )
        for part in seqc_tracker.loop_stack_generators:
            for generator in part:
                seq_c_generators.append(generator)
        _logger.debug(
            "***  collected generators, seq_c_generators: %s", seq_c_generators
        )

        main_generator = compress_generators_rle(
            seq_c_generators, declarations_generator
        )

        if main_generator.needs_play_zero_counter():
            declarations_generator.add_variable_declaration(
                main_generator.play_zero_counter_variable_name()
            )
        seq_c_generator = SeqCGenerator()
        seq_c_generator.append_statements_from(declarations_generator)
        seq_c_generator.append_statements_from(main_generator)

        if signal_obj.trigger_mode == TriggerMode.DIO_TRIGGER and awg.awg_number == 0:
            seq_c_generator.add_function_call_statement("setDIO", ["0"])

        seq_c_text = seq_c_generator.generate_seq_c()

        for line in seq_c_text.splitlines():
            _logger.debug(line)

        self._src.append({"filename": filename, "text": seq_c_text})
        self._wave_indices_all.append(
            {
                "filename": os.path.splitext(filename)[0] + "_waveindices.csv",
                "value": wave_indices.wave_indices(),
            }
        )
        if use_command_table:
            self._command_tables.append(
                {"seqc": filename, "ct": command_table_tracker.command_table()}
            )

    def waveform_size_hints(self, device: DeviceType):
        settings = self._settings
        if device == DeviceType.HDAWG:
            return settings.HDAWG_MIN_PLAYWAVE_HINT, settings.HDAWG_MIN_PLAYZERO_HINT
        if device == DeviceType.UHFQA:
            return settings.UHFQA_MIN_PLAYWAVE_HINT, settings.UHFQA_MIN_PLAYZERO_HINT
        if device == DeviceType.SHFQA:
            return settings.SHFQA_MIN_PLAYWAVE_HINT, settings.SHFQA_MIN_PLAYZERO_HINT
        if device == DeviceType.SHFSG:
            return settings.SHFSG_MIN_PLAYWAVE_HINT, settings.SHFSG_MIN_PLAYZERO_HINT

    def _sample_pulses(
        self,
        signal_id,
        interval_events,
        pulse_defs: Dict[str, PulseDef],
        sampling_rate,
        signal_type,
        device_type,
        oscillator_frequency,
        oscillator_frequencies_per_channel=None,
        multi_iq_signal=False,
    ):
        PHASE_RESOLUTION_RANGE = CodeGenerator.phase_resolution_range()
        signatures = set()
        for interval_event_list in interval_events.values():
            for interval_event in interval_event_list:
                signature: CodeGenerator.PlaybackSignature = interval_event[
                    "playback_signature"
                ]
                _logger.debug("Signature found %s in %s", signature, interval_event)
                signatures.add(signature)
        _logger.debug("Signatures: %s", signatures)

        sampled_signatures: Dict[CodeGenerator.WaveformSignature, Dict] = {}
        max_amplitude = 0.0
        needs_conjugate = device_type == DeviceType.SHFSG
        for signature in signatures:
            length = signature.waveform.length
            _logger.debug(
                "Sampling pulses for signature %s for signal %s, length %d device type %s",
                signature.waveform.signature_string()[0],
                signal_id,
                length,
                device_type.value,
            )

            if length % device_type.sample_multiple != 0:
                raise Exception(
                    f"Length of signature {signature.waveform.signature_string()[0]} is not divisible by {device_type.sample_multiple}, which it needs to be for {device_type.value}"
                )

            signature_pulse_map: Dict[str, PulseWaveformMap] = {}
            samples_i = np.zeros(length)
            samples_q = np.zeros(length)
            has_q = False
            for pulse_part in signature.waveform.pulses:
                _logger.debug(" Sampling pulse part %s", pulse_part)
                pulse_def = pulse_defs[pulse_part.pulse]
                _logger.debug(" Pulse def: %s", pulse_def)

                sampling_signal_type = signal_type
                if pulse_part.channel is not None:
                    sampling_signal_type = "single"
                if multi_iq_signal:
                    sampling_signal_type = "iq"
                if pulse_part.sub_channel is not None:
                    sampling_signal_type = "iq"

                amplitude = pulse_def.effective_amplitude

                amplitude_multiplier = 1.0
                if pulse_part.amplitude is not None:
                    amplitude_multiplier = pulse_part.amplitude

                if device_type == DeviceType.UHFQA and signal_type == "iq":
                    amplitude_multiplier *= math.sqrt(2)

                amplitude *= amplitude_multiplier

                if abs(amplitude) > max_amplitude:
                    max_amplitude = abs(amplitude)

                oscillator_phase = None
                if pulse_part.oscillator_phase is not None:
                    oscillator_phase = (
                        2
                        * math.pi
                        * pulse_part.oscillator_phase
                        / PHASE_RESOLUTION_RANGE
                    )

                baseband_phase = None
                if pulse_part.baseband_phase is not None:
                    baseband_phase = (
                        2 * math.pi * pulse_part.baseband_phase / PHASE_RESOLUTION_RANGE
                    )

                used_oscillator_frequency = oscillator_frequency
                if (
                    oscillator_frequencies_per_channel is not None
                    and pulse_part.channel is not None
                ):
                    used_oscillator_frequency = oscillator_frequencies_per_channel[
                        pulse_part.channel
                    ]
                _logger.debug(
                    " Sampling pulse %s using oscillator frequency %s",
                    pulse_part,
                    used_oscillator_frequency,
                )

                if used_oscillator_frequency and device_type == DeviceType.SHFSG:
                    amplitude /= math.sqrt(2)
                    amplitude_multiplier /= math.sqrt(2)

                iq_phase = pulse_part.iq_phase
                if iq_phase is None:
                    iq_phase = 0.0

                # In case oscillator phase can't be set at runtime (e.g. HW oscillator without
                # phase control from a sequencer), apply oscillator phase on a baseband (iq) signal
                if baseband_phase is not None:
                    # negation is necessary to get the right behavior, same as with "phase" below
                    iq_phase -= baseband_phase

                if pulse_part.phase is not None:
                    float_phase = phase_int_to_float(pulse_part.phase)
                    # According to "LabOne Q Software: Signal, channel and oscillator concept" REQ 1.3
                    iq_phase -= float_phase % (2 * math.pi)

                iq_phase = normalize_phase(iq_phase)

                samples = pulse_def.samples

                complex_modulation = True
                if device_type == DeviceType.UHFQA:
                    complex_modulation = False

                sampled_pulse = sample_pulse(
                    signal_type=sampling_signal_type,
                    sampling_rate=sampling_rate,
                    amplitude=amplitude,
                    length=pulse_part.pulse_samples / sampling_rate,
                    pulse_function=pulse_def.function,
                    modulation_frequency=used_oscillator_frequency,
                    modulation_phase=oscillator_phase,
                    iq_phase=iq_phase,
                    samples=samples,
                    complex_modulation=complex_modulation,
                    pulse_parameters=None
                    if pulse_part.pulse_parameters is None
                    else {k: v for k, v in pulse_part.pulse_parameters},
                )

                if "samples_q" in sampled_pulse and len(
                    sampled_pulse["samples_i"]
                ) != len(sampled_pulse["samples_q"]):
                    _logger.warning(
                        "Expected samples_q and samples_i to be of equal length"
                    )
                len_i = len(sampled_pulse["samples_i"])
                if not len_i == pulse_part.pulse_samples and samples is None:
                    num_samples = length_to_samples(pulse_def.length, sampling_rate)
                    _logger.warning(
                        "Pulse part %s: Expected %d samples but got %d; length = %f num samples=%d length in samples=%d",
                        repr(pulse_part),
                        pulse_part.pulse_samples,
                        len_i,
                        pulse_def.length,
                        num_samples,
                        pulse_def.length * sampling_rate,
                    )
                    raise Exception("Len mismatch")

                if (
                    pulse_part.channel == 0
                    and not multi_iq_signal
                    and not device_type == DeviceType.SHFQA
                ):
                    self.stencil_samples(
                        pulse_part.start, sampled_pulse["samples_i"], samples_i
                    )
                    has_q = True
                elif (
                    pulse_part.channel == 1
                    and not multi_iq_signal
                    and not device_type == DeviceType.SHFQA
                ):
                    self.stencil_samples(
                        pulse_part.start, sampled_pulse["samples_i"], samples_q
                    )
                    has_q = True
                else:
                    self.stencil_samples(
                        pulse_part.start, sampled_pulse["samples_i"], samples_i
                    )
                    if "samples_q" in sampled_pulse:
                        self.stencil_samples(
                            pulse_part.start,
                            sampled_pulse["samples_q"],
                            samples_q,
                        )
                        has_q = True

                pm = signature_pulse_map.get(pulse_def.id)
                if pm is None:
                    pm = PulseWaveformMap(
                        sampling_rate=sampling_rate,
                        length_samples=pulse_part.pulse_samples,
                        signal_type=sampling_signal_type,
                        complex_modulation=complex_modulation,
                    )
                    signature_pulse_map[pulse_def.id] = pm
                pm.instances.append(
                    PulseInstance(
                        offset_samples=pulse_part.start,
                        amplitude=amplitude_multiplier,
                        modulation_frequency=used_oscillator_frequency,
                        modulation_phase=oscillator_phase,
                        iq_phase=iq_phase,
                        channel=pulse_part.channel,
                        needs_conjugate=needs_conjugate,
                        pulse_parameters=None
                        if pulse_part.pulse_parameters is None
                        else {k: v for k, v in pulse_part.pulse_parameters},
                    )
                )

            sampled_pulse_obj = {
                "signature_pulse_map": signature_pulse_map,
                "samples_i": samples_i,
            }
            if len(samples_i) != length:
                _logger.warning(
                    "Num samples does not match. Expected %d but got %d",
                    length,
                    len(samples_i),
                )
            if has_q:
                if needs_conjugate:
                    samples_q = -samples_q
                sampled_pulse_obj["samples_q"] = samples_q

            if max_amplitude > 1e-9:
                sampled_signatures[signature.waveform] = sampled_pulse_obj

        return sampled_signatures

    def waves(self):
        return self._waves

    def src(self):
        return self._src

    def wave_indices(self):
        return self._wave_indices_all

    def command_tables(self):
        return self._command_tables

    def pulse_map(self) -> Dict[str, PulseMapEntry]:
        return self._pulse_map

    @staticmethod
    def sort_events(events):
        # For events that happen at the same sample, emit the play wave first, because it is asynchronous
        later = {
            "sequencer_start": -100,
            "initial_reset_phase": -4,
            "LOOP_STEP_START": -3,
            "PUSH_LOOP": -2,
            "reset_phase": -1,
            "acquire": 1,
            "ITERATE": 2,
        }
        sampled_event_list = sorted(
            events,
            key=lambda x: later[x["signature"]] if x["signature"] in later else 0,
        )

        return sampled_event_list

    @staticmethod
    def stencil_samples(start, source, target):
        source_start = 0
        target_start = start
        if start < 0:
            source_start = -start
            target_start = 0

        source_end = len(source)
        if source_end - source_start + target_start > len(target):
            source_end = source_start + len(target) - target_start
        target_end = target_start + source_end - source_start
        if target_end >= 0 and target_start < len(target):
            to_insert = source[source_start:source_end]
            target[target_start:target_end] += to_insert
        else:
            _logger.debug(
                "Not inserting: %d:%d , %d:%d",
                source_start,
                source_end,
                target_start,
                target_end,
            )

    @staticmethod
    def phase_resolution_range():
        return round(math.pow(2, CodeGenerator.PHASE_RESOLUTION_BITS))

    @staticmethod
    def post_process_sampled_events(awg: AWGInfo, sampled_events):
        if awg.device_type == DeviceType.SHFQA:
            has_acquire = False
            for sampled_event_list in sampled_events.values():
                for x in sampled_event_list:
                    if x["signature"] == "acquire":
                        has_acquire = True
                        break

            for sampled_event_list in sampled_events.values():
                start = None
                end = None
                acquisition_types = set()
                play = []
                acquire = []
                for x in sampled_event_list:
                    if "signal_id" in x and x["signature"] != "acquire":
                        play.append(x)
                        start = x["start"]
                        end = x["end"] if end is None else max(end, x["end"])
                    elif x["signature"] == "acquire":
                        start = x["start"]
                        if "acquisition_type" in x:
                            acquisition_types.update(x["acquisition_type"])
                        acquire.append(x)
                        end = x["end"] if end is None else max(end, x["end"])
                if len(play) > 0 and len(acquire) == 0 and has_acquire:
                    _logger.warning("Problem:")
                    for log_event in sampled_event_list:
                        _logger.warning("  %s", log_event)
                    raise Exception(f"Play and acquire must happen at the same time")
                if len(play) > 0 or len(acquire) > 0:
                    end = (
                        round(end / DeviceType.SHFQA.sample_multiple)
                        * DeviceType.SHFQA.sample_multiple
                    )
                    qa_event = {
                        "signature": "QA_EVENT",
                        "acquire_events": acquire,
                        "play_events": play,
                        "start": start,
                        "end": end,
                        "acquisition_type": list(acquisition_types),
                    }

                    for to_delete in play + acquire:
                        sampled_event_list.remove(to_delete)
                    sampled_event_list.append(qa_event)

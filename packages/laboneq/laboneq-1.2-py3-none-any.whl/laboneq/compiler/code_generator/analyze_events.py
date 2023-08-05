# Copyright 2022 Zurich Instruments AG
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import logging
import math
from dataclasses import dataclass
from typing import List, Any, Optional, Dict, Tuple, TYPE_CHECKING

from engineering_notation import EngNumber
from intervaltree import IntervalTree
from sortedcontainers import SortedDict

from laboneq.compiler.awg_info import AWGInfo
from laboneq.compiler.awg_signal_type import AWGSignalType
from laboneq.compiler.code_generator.dict_list import add_to_dict_list, merge_dict_list
from laboneq.compiler.code_generator.interval_calculator import (
    MinimumWaveformLengthViolation,
    calculate_intervals,
)
from laboneq.compiler.code_generator.signatures import (
    PlaybackSignature,
    WaveformSignature,
    PulseSignature,
)
from laboneq.compiler.code_generator.utils import normalize_phase
from laboneq.compiler.device_type import DeviceType
from laboneq.compiler.event_graph import EventType
from laboneq.core.exceptions import LabOneQException
from laboneq.core.utilities.pulse_sampler import length_to_samples, interval_to_samples

if TYPE_CHECKING:
    from laboneq.compiler.code_generator import SignalObj

_logger = logging.getLogger(__name__)


def analyze_loop_times(
    awg: AWGInfo,
    events: List[Any],
    sampling_rate: float,
    delay: float,
) -> SortedDict:
    retval = SortedDict()

    plays_anything = False
    signal_ids = [signal_obj.id for signal_obj in awg.signals]
    for e in events:
        if (
            e["event_type"] in ["PLAY_START", "ACQUIRE_START"]
            and e.get("signal") in signal_ids
        ):
            plays_anything = True
            break

    if plays_anything:
        _logger.debug(
            "Analyzing loop events for awg %d of %s", awg.awg_number, awg.device_id
        )
    else:
        _logger.debug(
            "Skipping analysis of loop events for awg %d of %s because nothing is played",
            awg.awg_number,
            awg.device_id,
        )
        return retval

    loop_step_start_events = [
        event for event in events if event["event_type"] == "LOOP_STEP_START"
    ]
    loop_step_end_events = [
        event for event in events if event["event_type"] == "LOOP_STEP_END"
    ]
    loop_iteration_events = [
        event
        for event in events
        if event["event_type"] == "LOOP_ITERATION_END"
        and "compressed" in event
        and event["compressed"]
    ]

    compressed_sections = set(
        [event["section_name"] for event in loop_iteration_events]
    )
    section_repeats = {}
    for event in loop_iteration_events:
        if "num_repeats" in event:
            section_repeats[event["section_name"]] = event["num_repeats"]

    _logger.debug("Found %d loop step start events", len(loop_step_start_events))
    events_already_added = set()
    for event in loop_step_start_events:
        _logger.debug("  loop timing: processing  %s", event)

        event_time_in_samples = length_to_samples(event["time"] + delay, sampling_rate)
        loop_event = {
            "signature": "LOOP_STEP_START",
            "nesting_level": event["nesting_level"],
            "loop_id": event["section_name"],
            "start": event_time_in_samples,
            "end": event_time_in_samples,
        }

        if event["section_name"] not in compressed_sections:
            frozen = frozenset(loop_event.items())
            if frozen not in events_already_added:
                add_to_dict_list(retval, event_time_in_samples, loop_event)
                events_already_added.add(frozen)
                _logger.debug("Added %s", loop_event)
            else:
                _logger.debug("SKIP adding double %s", loop_event)
        elif event["iteration"] == 0:
            push_event = {
                "signature": "PUSH_LOOP",
                "nesting_level": event["nesting_level"],
                "start": event_time_in_samples,
                "end": event_time_in_samples,
                "loop_id": event["section_name"],
            }
            if event["section_name"] in section_repeats:
                push_event["num_repeats"] = section_repeats[event["section_name"]]
            add_to_dict_list(retval, event_time_in_samples, push_event)
            _logger.debug("Added %s", push_event)

    _logger.debug("Found %d loop step end events", len(loop_step_end_events))
    for event in loop_step_end_events:
        event_time_in_samples = length_to_samples(event["time"] + delay, sampling_rate)
        loop_event = {
            "signature": "LOOP_STEP_END",
            "nesting_level": event["nesting_level"],
            "loop_id": event["section_name"],
            "start": event_time_in_samples,
            "end": event_time_in_samples,
        }

        if event["section_name"] not in compressed_sections:
            frozen = frozenset(loop_event.items())
            if frozen not in events_already_added:
                add_to_dict_list(retval, event_time_in_samples, loop_event)
                events_already_added.add(frozen)
                _logger.debug("Added %s", loop_event)
            else:
                _logger.debug("SKIP adding double %s", loop_event)

    for event in loop_iteration_events:
        event_time_in_samples = length_to_samples(event["time"] + delay, sampling_rate)
        iteration_event = {
            "signature": "ITERATE",
            "nesting_level": event["nesting_level"],
            "start": event_time_in_samples,
            "end": event_time_in_samples,
            "loop_id": event["section_name"],
        }

        if event["section_name"] in section_repeats:
            iteration_event["num_repeats"] = section_repeats[event["section_name"]]

        add_to_dict_list(retval, event_time_in_samples, iteration_event)
        _logger.debug("Added %s", iteration_event)

        if event_time_in_samples % awg.device_type.sample_multiple != 0:
            _logger.warning(
                "Event %s: event_time_in_samples %f at sampling rate %s is not divisible by %d",
                event,
                event_time_in_samples,
                EngNumber(sampling_rate),
                awg.device_type.sample_multiple,
            )

    return retval


def analyze_init_times(
    device_id: str, sampling_rate: float, delay: float
) -> SortedDict:
    _logger.debug("Analyzing init events for device %s", device_id)
    retval = SortedDict()
    delay_samples = length_to_samples(delay, sampling_rate)
    add_to_dict_list(
        retval,
        delay_samples,
        {
            "device_id": device_id,
            "start": delay_samples,
            "signature": "sequencer_start",
            "end": delay_samples,
        },
    )
    return retval


def analyze_precomp_reset_times(
    events: List[Any],
    device_id: str,
    sampling_rate: float,
    delay: float,
):
    retval = SortedDict()
    for event in events:
        if (
            event.get("device_id", None) != device_id
            or event["event_type"] != EventType.RESET_PRECOMPENSATION_FILTERS
        ):
            continue
        event_time_in_samples = length_to_samples(event["time"] + delay, sampling_rate)
        init_event = {
            "start": event_time_in_samples,
            "signature": "reset_precompensation_filters",
            "end": event_time_in_samples,
            "device_id": device_id,
            "signal_id": event.get("signal_id"),
        }

        add_to_dict_list(retval, event_time_in_samples, init_event)
    return retval


def analyze_phase_reset_times(
    events: List[Any],
    device_id: str,
    sampling_rate: float,
    delay: float,
):
    retval = SortedDict()
    reset_phase_events = [
        event
        for event in events
        if event["event_type"]
        in (
            EventType.RESET_HW_OSCILLATOR_PHASE,
            EventType.INITIAL_RESET_HW_OSCILLATOR_PHASE,
        )
        and "device_id" in event
        and event["device_id"] == device_id
    ]
    for event in reset_phase_events:
        event_time_in_samples = length_to_samples(event["time"] + delay, sampling_rate)
        signature = (
            "reset_phase"
            if event["event_type"] == EventType.RESET_HW_OSCILLATOR_PHASE
            else "initial_reset_phase"
        )
        init_event = {
            "start": event_time_in_samples,
            "signature": signature,
            "end": event_time_in_samples,
            "device_id": device_id,
        }

        add_to_dict_list(retval, event_time_in_samples, init_event)
    return retval


def analyze_set_oscillator_times(
    events: List,
    signal_id: str,
    device_id: str,
    device_type: DeviceType,
    sampling_rate: float,
    delay: float,
) -> SortedDict:
    set_oscillator_events = [
        event
        for event in events
        if event["event_type"] == "SET_OSCILLATOR_FREQUENCY_START"
        and event.get("device_id") == device_id
        and event.get("signal") == signal_id
    ]
    if len(set_oscillator_events) == 0:
        return SortedDict()

    if device_type not in (DeviceType.SHFQA, DeviceType.SHFSG):
        raise LabOneQException(
            "Real-time frequency sweep only supported on SHF devices"
        )

    iterations = {event["iteration"]: event for event in set_oscillator_events}
    assert list(iterations.keys()) == list(
        range(len(iterations))
    )  # "iteration" values are unique, ordered, and numbered 0 .. N-1
    start_frequency = iterations[0]["value"]
    step_frequency = iterations[1]["value"] - start_frequency

    retval = SortedDict()

    for iteration, event in iterations.items():
        if (
            abs(event["value"] - iteration * step_frequency - start_frequency)
            > 1e-3  # tolerance: 1 mHz
        ):
            raise LabOneQException("Realtime oscillator sweeps must be linear")

        event_time_in_samples = length_to_samples(event["time"] + delay, sampling_rate)
        set_oscillator_event = {
            "start": event_time_in_samples,
            "start_frequency": start_frequency,
            "step_frequency": step_frequency,
            "signature": "set_oscillator_frequency",
            "parameter_name": event["parameter"]["id"],
            "iteration": iteration,
        }

        add_to_dict_list(retval, event_time_in_samples, set_oscillator_event)

    return retval


def analyze_acquire_times(
    events: List[Any],
    signal_id: str,
    sampling_rate: float,
    delay: float,
    sample_multiple: int,
    channels,
) -> SortedDict:
    retval = SortedDict()

    _logger.debug(
        "Calculating acquire times for signal %s with delay %s ( %s samples)",
        signal_id,
        str(delay),
        str(round(delay * sampling_rate)),
    )

    @dataclass
    class IntervalStartEvent:
        event_type: str
        time: float
        play_wave_id: str
        acquisition_type: list
        pulse_parameters: Optional[Dict[str, Any]]

    @dataclass
    class IntervalEndEvent:
        event_type: str
        time: float
        play_wave_id: str

    interval_zip = list(
        zip(
            [
                IntervalStartEvent(
                    event["event_type"],
                    event["time"] + delay,
                    event["play_wave_id"],
                    event.get("acquisition_type", []),
                    event.get("pulse_parameters"),
                )
                for event in events
                if event["event_type"] in ["ACQUIRE_START"]
                and event["signal"] == signal_id
            ],
            [
                IntervalEndEvent(
                    event["event_type"],
                    event["time"] + delay,
                    event["play_wave_id"],
                )
                for event in events
                if event["event_type"] in ["ACQUIRE_END"]
                and event["signal"] == signal_id
            ],
        )
    )

    for interval_start, interval_end in interval_zip:
        start_samples, end_samples = interval_to_samples(
            interval_start.time, interval_end.time, sampling_rate
        )
        if start_samples % sample_multiple != 0:
            start_samples = (
                math.floor(start_samples / sample_multiple) * sample_multiple
            )

        if end_samples % sample_multiple != 0:
            end_samples = math.floor(end_samples / sample_multiple) * sample_multiple

        acquire_event = {
            "start": start_samples,
            "signature": "acquire",
            "end": end_samples,
            "signal_id": signal_id,
            "play_wave_id": interval_start.play_wave_id,
            "acquisition_type": interval_start.acquisition_type,
            "channels": channels,
            "pulse_parameters": interval_start.pulse_parameters,
        }

        add_to_dict_list(retval, acquire_event["start"], acquire_event)

    return retval


def analyze_oscillator_switch_events(
    signals: Dict[str, SignalObj],
    events: List[Dict],
    signal_ids: List[str],
    sampling_rate: float,
    granularity: int,
    delay: float,
):
    osc_switch_events = SortedDict()
    hw_oscillators = {
        signal_id: signals[signal_id].hw_oscillator for signal_id in signal_ids
    }
    hw_oscs_values = set(hw_oscillators.values())
    awg = signals[signal_ids[0]].awg
    device_type = awg.device_type
    if device_type == DeviceType.HDAWG:
        if awg.signal_type == AWGSignalType.DOUBLE:
            # Skip for now. In double mode, 2 oscillators may (?) be active.
            # todo (PW): Do we support dual HW modulated RF signals?
            return osc_switch_events
    if not device_type.supports_oscillator_switching:
        if len(hw_oscs_values) > 1:
            raise LabOneQException(
                f"Attempting to multiplex several HW-modulated signals "
                f"({', '.join(signal_ids)}) on {device_type.value}, which does not "
                f"support oscillator switching."
            )
    if len(hw_oscs_values) <= 1:
        return osc_switch_events

    if None in hw_oscs_values:
        missing_oscillator_signal = next(
            signal_id for signal_id, osc in hw_oscillators.items() if osc is None
        )
        del hw_oscillators[missing_oscillator_signal]
        other_signals = set(hw_oscillators.keys())
        raise LabOneQException(
            f"Attempting to multiplex HW-modulated signal(s) "
            f"({', '.join(other_signals)}) "
            f"with signal that is not HW modulated ({missing_oscillator_signal})."
        )

    active_osc = None
    active_play_segments = set()

    for event in events:
        if event.get("signal") not in signal_ids:
            continue
        signal_id = event["signal"]
        event_time_in_samples = length_to_samples(event["time"] + delay, sampling_rate)
        if event["event_type"] == EventType.PLAY_START:
            if active_osc is not None:
                raise LabOneQException(
                    f"Conflicting HW oscillators on signals {', '.join(signal_ids)}"
                )
            active_osc = hw_oscillators.get(signal_id)
            active_play_segments.add(event["chain_element_id"])

            # Round down to sequencer grid. Collisions with other playback will be
            # detected downstream when calculating waveform intervals.
            osc_switch_time = event_time_in_samples // granularity * granularity

            osc_switch_event = {
                "signature": "switch_oscillator",
                "start": osc_switch_time,
                "oscillator": active_osc,
                "signal": signal_id,
                "section_name": event["section_name"],
                "play_wave_id": event["play_wave_id"],
            }
            add_to_dict_list(osc_switch_events, osc_switch_time, osc_switch_event)
        elif event["event_type"] == EventType.PLAY_END:
            active_play_segments.remove(event["chain_element_id"])
            if len(active_play_segments) == 0:
                active_osc = None
    return osc_switch_events


def analyze_play_wave_times(
    events: List[Dict],
    signals: Dict[str, SignalObj],
    signal_ids: List[str],
    device_type: DeviceType,
    sampling_rate,
    delay: float,
    other_events: Dict,
    iq_phase: float,
    waveform_size_hints: Tuple[int, int],
    phase_resolution_range: float,
    sub_channel: Optional[int] = None,
):
    sample_multiple = device_type.sample_multiple
    min_play_wave = device_type.min_play_wave
    play_wave_size_hint, play_zero_size_hint = waveform_size_hints
    signal_id = "_".join(signal_ids)
    for k, v in other_events.items():
        _logger.debug("Signal %s other event %s %s", signal_id, k, v)

    if sub_channel is not None:
        _logger.debug("Signal %s: using sub_channel = %s", signal_id, sub_channel)

    @dataclass
    class IntervalStartEvent:
        event_type: str
        time: float
        play_wave_id: str
        amplitude: float
        index: int
        oscillator_phase: Optional[float]
        phase: Optional[float]
        sub_channel: Optional[int]
        baseband_phase: Optional[float]
        pulse_parameters: Optional[Dict[str, Any]]

    @dataclass
    class IntervalEndEvent:
        event_type: str
        time: float
        play_wave_id: str
        index: int

    @dataclass
    class IntervalData:
        pulse: str
        index: int
        amplitude: float
        channel: int
        oscillator_phase: float
        baseband_phase: float
        phase: float
        sub_channel: int
        pulse_parameters: Optional[Dict[str, Any]]

    interval_zip: List[Tuple[IntervalStartEvent, IntervalEndEvent]] = []
    for index, cur_signal_id in enumerate(signal_ids):
        interval_zip.extend(
            zip(
                [
                    IntervalStartEvent(
                        event["event_type"],
                        event["time"] + delay,
                        event["play_wave_id"],
                        event["amplitude"],
                        index,
                        event.get("oscillator_phase"),
                        event.get("phase"),
                        sub_channel,
                        event.get("baseband_phase"),
                        event.get("pulse_parameters"),
                    )
                    for event in events
                    if event["event_type"] in ["PLAY_START"]
                    and event["signal"] == cur_signal_id
                ],
                [
                    IntervalEndEvent(
                        event["event_type"],
                        event["time"] + delay,
                        event["play_wave_id"],
                        index,
                    )
                    for event in events
                    if event["event_type"] in ["PLAY_END"]
                    and event["signal"] == cur_signal_id
                ],
            )
        )
    if len(interval_zip) > 0:
        _logger.debug(
            "Analyzing play wave timings for %d play wave events on signals %s",
            len(interval_zip),
            signal_ids,
        )

    for ivzip in interval_zip:
        _logger.debug("Signal %s interval zip: %s", signal_id, ivzip)

    t = IntervalTree()
    PHASE_RESOLUTION_RANGE = phase_resolution_range
    for index, (interval_start, interval_end) in enumerate(interval_zip):
        oscillator_phase = None
        if interval_start.oscillator_phase is not None:
            oscillator_phase = math.floor(
                normalize_phase(interval_start.oscillator_phase)
                / 2
                / math.pi
                * PHASE_RESOLUTION_RANGE
            )

        baseband_phase = None
        if interval_start.baseband_phase is not None:
            baseband_phase = math.floor(
                normalize_phase(interval_start.baseband_phase)
                / 2
                / math.pi
                * PHASE_RESOLUTION_RANGE
            )
        start_samples, end_samples = interval_to_samples(
            interval_start.time, interval_end.time, sampling_rate
        )
        if start_samples != end_samples:
            t.addi(
                start_samples,
                end_samples,
                IntervalData(
                    pulse=interval_start.play_wave_id,
                    index=index,
                    amplitude=interval_start.amplitude,
                    channel=interval_start.index,
                    oscillator_phase=oscillator_phase,
                    baseband_phase=baseband_phase,
                    phase=interval_start.phase,
                    sub_channel=interval_start.sub_channel,
                    pulse_parameters=interval_start.pulse_parameters,
                ),
            )

        else:
            _logger.debug(
                "Skipping interval %s because it is zero length (from %s samples to %s samples) ",
                interval_start.play_wave_id,
                start_samples,
                end_samples,
            )

    for ivs in sorted(t.items()):
        _logger.debug("Signal %s intervaltree:%s", signal_id, ivs)

    oscillator_switch_events = analyze_oscillator_switch_events(
        signals, events, signal_ids, sampling_rate, sample_multiple, delay
    )

    merge_dict_list(other_events, oscillator_switch_events)

    cut_points = set()
    for event_time, other_event_list in other_events.items():
        intervals = [
            interval for interval in t.at(event_time) if interval.begin < event_time
        ]

        if len(intervals) > 0:
            try:
                other_event = next(
                    e for e in other_event_list if e["signature"] == "switch_oscillator"
                )
                section = other_event["section_name"]
                pulse = other_event["play_wave_id"]
                signal_name = other_event["signal"]
                raise LabOneQException(
                    f"In section {section}, pulse {pulse}, on signal {signal_name}: "
                    f"cannot switch oscillator because the event intersects with "
                    f"other playback."
                )
            except StopIteration:
                pass
            raise RuntimeError(
                f"Events {other_event_list} intersect playWave intervals {intervals}"
            )
        else:
            cut_points.add(event_time)

    sequence_end = length_to_samples(events[-1]["time"] + delay, sampling_rate)
    sequence_end += play_wave_size_hint + play_zero_size_hint  # slack
    sequence_end += (-sequence_end) % sample_multiple  # align to sequencer grid
    cut_points.add(sequence_end)

    cut_points = sorted(list(cut_points))

    _logger.debug(
        "Collecting pulses to ensure waveform lengths are above the minimum of %d "
        "samples and are a multiple of %d samples for signal %s",
        min_play_wave,
        sample_multiple,
        signal_id,
    )

    try:
        compacted_intervals = calculate_intervals(
            t,
            min_play_wave,
            play_wave_size_hint,
            play_zero_size_hint,
            cut_points,
            granularity=sample_multiple,
        )
    except MinimumWaveformLengthViolation as e:
        raise LabOneQException(
            f"Failed to map the scheduled pulses to seqC without violating the "
            f"minimum waveform size {min_play_wave} of device "
            f"'{device_type.value}'.\n"
            f"Suggested workaround: manually add delays to overly short loops, etc."
        ) from e

    oscillator_intervals = IntervalTree()
    start = 0
    active_oscillator = None
    for osc_event_time, osc_event in oscillator_switch_events.items():
        oscillator_intervals.addi(
            start, osc_event_time, {"oscillator": active_oscillator}
        )
        active_oscillator = osc_event[0]["oscillator"]
        start = osc_event_time
    oscillator_intervals.addi(start, sequence_end, {"oscillator": active_oscillator})

    interval_events = SortedDict()

    signatures = set()

    _logger.debug("Calculating waveform signatures for signal %s", signal_id)

    for k in sorted(compacted_intervals.items()):
        _logger.debug("Calculating signature for %s and its children", k)

        overlap = t.overlap(k.begin, k.end)
        _logger.debug("Overlap is %s", overlap)

        v = sorted(t.overlap(k.begin, k.end))

        hw_oscillator = oscillator_intervals.overlap(k)
        assert len(hw_oscillator) == 1
        hw_oscillator = next(iter(hw_oscillator)).data["oscillator"]

        signature_pulses = []
        has_child = False
        for iv in sorted(v, key=lambda x: (x.begin, x.data.channel)):
            data: IntervalData = iv.data
            _logger.debug("Calculating looking at child %s", iv)
            has_child = True
            start = iv.begin - k.begin
            end = iv.end - k.begin
            float_phase = data.phase
            if float_phase is not None:
                float_phase = normalize_phase(float_phase)

                int_phase = phase_float_to_int(float_phase)
            else:
                int_phase = None

            signature_pulses.append(
                PulseSignature(
                    start=start,
                    end=end,
                    pulse=data.pulse,
                    pulse_samples=iv.length(),
                    amplitude=data.amplitude,
                    phase=int_phase,
                    oscillator_phase=data.oscillator_phase,
                    baseband_phase=data.baseband_phase,
                    iq_phase=iq_phase,
                    channel=data.channel if len(signal_ids) > 1 else None,
                    sub_channel=data.sub_channel,
                    pulse_parameters=None
                    if data.pulse_parameters is None
                    else frozenset(data.pulse_parameters.items()),
                )
            )

        waveform_signature = WaveformSignature(k.length(), tuple(signature_pulses))
        signature = PlaybackSignature(waveform_signature, hw_oscillator)

        if has_child:
            signatures.add(signature)
            start = k.begin
            interval_event = {
                "start": start,
                "signature": "playwave",
                "playback_signature": signature,
                "end": k.end,
                "signal_id": signal_id,
            }
            add_to_dict_list(interval_events, start, interval_event)

    if len(signatures) > 0:
        _logger.debug(
            "Signatures calculated: %d signatures for signal %s",
            len(signatures),
            signal_id,
        )
    for sig in signatures:
        _logger.debug(sig)
    _logger.debug("Interval events: %s", interval_events)

    return interval_events


PHASE_FIXED_SCALE = 1000000000


def phase_float_to_int(phase: float):
    return int(PHASE_FIXED_SCALE * phase / 2 / math.pi)


def phase_int_to_float(phase: int):
    return (float(phase * math.pi * 2) / PHASE_FIXED_SCALE) % (2 * math.pi)

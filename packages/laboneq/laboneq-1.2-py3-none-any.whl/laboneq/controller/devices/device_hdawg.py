# Copyright 2019 Zurich Instruments AG
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import json
import time
from enum import IntEnum
from typing import Any, Dict, List, Tuple, TYPE_CHECKING, Optional
import numpy as np

from laboneq.controller.communication import (
    DaqNodeAction,
    DaqNodeSetAction,
    DaqNodeGetAction,
    CachingStrategy,
)
from laboneq.controller.devices.device_zi import DeviceZI
from laboneq.controller.recipe_1_4_0 import Initialization
from laboneq.controller.recipe_enums import ReferenceClockSource
from laboneq.controller.recipe_enums import SignalType, DIOConfigType
from laboneq.controller.recipe_processor import DeviceRecipeData, RecipeData
from laboneq.controller.util import LabOneQControllerException
from laboneq.controller.versioning import LabOneVersion
from laboneq.core.exceptions.laboneq_exception import LabOneQException
from laboneq.core.types.enums.acquisition_type import AcquisitionType

DIG_TRIGGER_1_LEVEL = 0.225

DELAY_NODE_GRANULARITY_SAMPLES = 1
DELAY_NODE_MAX_SAMPLES = 62
DEFAULT_SAMPLE_FREQUENCY_HZ = 2.4e9

REFERENCE_CLOCK_SOURCE_INTERNAL = 0
REFERENCE_CLOCK_SOURCE_EXTERNAL = 1
REFERENCE_CLOCK_SOURCE_ZSYNC = 2


class ModulationMode(IntEnum):
    OFF = 0
    SINE_00 = 1
    SINE_11 = 2
    SINE_01 = 3
    SINE_10 = 4
    ADVANCED = 5
    MIXER_CAL = 6


class DeviceHDAWG(DeviceZI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dev_type = "HDAWG8"
        self.dev_opts = ["MF", "ME", "SKW"]
        self._channels = 8
        self._multi_freq = True

    def _process_dev_opts(self):
        if self.dev_type == "HDAWG8":
            self._channels = 8
        elif self.dev_type == "HDAWG4":
            self._channels = 4
        else:
            self._logger.warning(
                "%s: Unknown device type '%s', assuming 4 channels device.",
                self.dev_repr,
                self.dev_type,
            )
            self._channels = 4

        self._multi_freq = "MF" in self.dev_opts

    def _get_num_AWGs(self):
        return self._channels // 2

    def _osc_group_by_channel(self, channel: int) -> int:
        # For LabOne Q SW, the AWG oscillator control is always on, in which
        # case every pair of output channels share the same set of oscillators
        return channel // 2

    def _get_next_osc_index(
        self, osc_group: int, previously_allocated: int
    ) -> Optional[int]:
        # With MF option 4 oscillators per channel pair are available,
        # and only 1 oscillator per channel pair without MF option.
        max_per_group = 4 if self._multi_freq else 1
        if previously_allocated >= max_per_group:
            return None
        osc_index_base = osc_group * max_per_group
        return osc_index_base + previously_allocated

    def _nodes_to_monitor_impl(self) -> List[str]:
        nodes = []
        for awg in range(self._get_num_AWGs()):
            nodes.append(f"/{self.serial}/awgs/{awg}/enable")
        return nodes

    def collect_awg_after_upload_nodes(self, initialization: Initialization.Data):
        nodes_to_configure_phase = []

        for awg in initialization.awgs or []:
            self._logger.debug(
                "%s: Configure modulation phase depending on IQ enabling on awg %d.",
                self.dev_repr,
                awg.awg,
            )
            nodes_to_configure_phase.append(
                DaqNodeSetAction(
                    self._daq,
                    f"/{self.serial}/sines/{awg.awg * 2}/phaseshift",
                    90 if (awg.signal_type == SignalType.IQ) else 0,
                )
            )

            nodes_to_configure_phase.append(
                DaqNodeSetAction(
                    self._daq, f"/{self.serial}/sines/{awg.awg * 2 + 1}/phaseshift", 0
                )
            )

        return nodes_to_configure_phase

    def conditions_for_execution_ready(self) -> Dict[str, Any]:
        conditions: Dict[str, Any] = {}
        for awg_index in self._allocated_awgs:
            conditions[f"/{self.serial}/awgs/{awg_index}/enable"] = 1
        return conditions

    def conditions_for_execution_done(
        self, acquisition_type: AcquisitionType
    ) -> Dict[str, Any]:
        conditions: Dict[str, Any] = {}
        for awg_index in self._allocated_awgs:
            conditions[f"/{self.serial}/awgs/{awg_index}/enable"] = 0
        return conditions

    def collect_output_initialization_nodes(
        self, device_recipe_data: DeviceRecipeData, initialization: Initialization.Data
    ) -> List[DaqNodeAction]:
        self._logger.debug("%s: Initializing device...", self.dev_repr)

        nodes: List[Tuple[str, Any]] = []

        # If we do not turn all channels off, we get the following error message from
        # the server/device: 'An error happened on device dev8330 during the execution
        # of the experiment. Error message: Reinitialized signal output delay on
        # channel 0 (numbered from 0)'
        #
        for channel in range(self._channels):
            nodes.append((f"sigouts/{channel}/on", 0))

        sampling_rate = initialization.config.sampling_rate
        if sampling_rate is None or sampling_rate == 0:
            sampling_rate = DEFAULT_SAMPLE_FREQUENCY_HZ
        nodes.append(("system/clocks/sampleclock/freq", sampling_rate))

        outputs = initialization.outputs or []
        for output in outputs:

            awg_idx = output.channel // 2
            self._allocated_awgs.add(awg_idx)

            nodes.append((f"sigouts/{output.channel}/on", 1 if output.enable else 0))
            nodes.append((f"sigouts/{output.channel}/offset", output.offset))
            nodes.append((f"awgs/{awg_idx}/single", 1))

            measurement_delay_rounded = (
                self._get_total_rounded_delay_samples(
                    output,
                    sampling_rate,
                    DELAY_NODE_GRANULARITY_SAMPLES,
                    DELAY_NODE_MAX_SAMPLES,
                    0,
                )
                / sampling_rate
            )

            nodes.append((f"sigouts/{output.channel}/delay", measurement_delay_rounded))

            awg_ch = output.channel % 2
            iq_idx = output.channel // 2
            iq_gains_mx = device_recipe_data.iq_settings.get(iq_idx, None)

            if iq_gains_mx is None:
                # Fall back to old behavior (suitable for single channel output)
                diagonal_channel_index = awg_ch
                off_diagonal_channel_index = int(not diagonal_channel_index)

                modulation_mode = (
                    (ModulationMode.SINE_00 if awg_ch == 0 else ModulationMode.SINE_11)
                    if output.modulation
                    else ModulationMode.OFF
                )
                nodes += [
                    (
                        f"awgs/{awg_idx}/outputs/{awg_ch}/modulation/mode",
                        modulation_mode,
                    ),
                    (
                        f"awgs/{awg_idx}/outputs/{awg_ch}/gains/{diagonal_channel_index}",
                        output.gains.diagonal,
                    ),
                    (
                        f"awgs/{awg_idx}/outputs/{awg_ch}/gains/{off_diagonal_channel_index}",
                        output.gains.off_diagonal,
                    ),
                ]
            else:
                # I/Q output
                modulation_mode = (
                    ModulationMode.MIXER_CAL
                    if output.modulation
                    else ModulationMode.OFF
                )
                nodes += [
                    (
                        f"awgs/{awg_idx}/outputs/{awg_ch}/modulation/mode",
                        modulation_mode,
                    ),
                    (
                        f"awgs/{awg_idx}/outputs/{awg_ch}/gains/0",
                        iq_gains_mx[0][awg_ch],
                    ),
                    (
                        f"awgs/{awg_idx}/outputs/{awg_ch}/gains/1",
                        iq_gains_mx[1][awg_ch],
                    ),
                ]

            precomp_p = f"sigouts/{output.channel}/precompensation/"
            try:
                precomp = output.precompensation
                if not precomp:
                    raise AttributeError
                nodes.append((precomp_p + "enable", 1))
                # Exponentials
                for e in range(8):
                    exp_p = precomp_p + f"exponentials/{e}/"
                    try:
                        exp = precomp["exponential"][e]
                        nodes += [
                            (exp_p + "enable", 1),
                            (exp_p + "timeconstant", exp["timeconstant"]),
                            (exp_p + "amplitude", exp["amplitude"]),
                        ]
                    except (KeyError, IndexError, TypeError):
                        nodes.append((exp_p + "enable", 0))
                # Bounce
                bounce_p = precomp_p + "bounces/0/"
                try:
                    bounce = precomp["bounce"]
                    delay = bounce["delay"]
                    amp = bounce["amplitude"]
                    nodes += [
                        (bounce_p + "enable", 1),
                        (bounce_p + "delay", delay),
                        (bounce_p + "amplitude", amp),
                    ]
                except (KeyError, TypeError):
                    nodes.append((bounce_p + "enable", 0))
                # Highpass
                hp_p = precomp_p + "highpass/0/"
                try:
                    hp = precomp["high_pass"]
                    timeconstant = hp["timeconstant"]
                    clearing = {"level": 0, "rise": 1, "fall": 2, "both": 3}[
                        hp["clearing"]
                    ]
                    nodes += [
                        (hp_p + "enable", 1),
                        (hp_p + "timeconstant", timeconstant),
                        (hp_p + "clearing/slope", clearing),
                    ]
                except (KeyError, TypeError):
                    nodes.append((hp_p + "enable", 0))
                # FIR
                fir_p = precomp_p + "fir/"
                try:
                    fir = np.array(precomp["FIR"]["coefficients"])
                    if len(fir) > 40:
                        raise LabOneQException(
                            "FIR coefficents must be a list of at most 40 doubles"
                        )
                    fir = np.concatenate((fir, np.zeros((40 - len(fir)))))
                    nodes += [(fir_p + "enable", 1), (fir_p + "coefficients", fir)]
                except (KeyError, IndexError, TypeError):
                    nodes.append((fir_p + "enable", 0))
            except (KeyError, TypeError, AttributeError):
                nodes.append((precomp_p + "enable", 0))

        osc_selects = {
            ch: osc.index for osc in self._allocated_oscs for ch in osc.channels
        }
        for ch, osc_idx in osc_selects.items():
            nodes.append((f"sines/{ch}/oscselect", osc_idx))

        return [DaqNodeSetAction(self._daq, f"/{self.serial}/{k}", v) for k, v in nodes]

    def wait_for_conditions_to_start(self):
        self._wait_for_node(
            f"/{self.serial}/system/clocks/sampleclock/status", 0, timeout=5
        )

    def collect_awg_before_upload_nodes(
        self, initialization: Initialization.Data, recipe_data: RecipeData
    ):
        device_specific_initialization_nodes = [
            DaqNodeSetAction(
                self._daq, f"/{self.serial}/system/awg/oscillatorcontrol", 1
            ),
            DaqNodeSetAction(
                self._daq, f"/{self.serial}/raw/system/awg/runtimechecks/enable", 1
            ),
        ]

        return device_specific_initialization_nodes

    def add_command_table_header(self, body: dict) -> Dict:
        return {
            "$schema": "https://docs.zhinst.com/hdawg/commandtable/v1_0/schema",
            "header": {"version": "1.0.0"},
            "table": body,
        }

    def command_table_path(self, awg_index: int) -> str:
        return f"/{self.serial}/awgs/{awg_index}/commandtable/"

    def collect_trigger_configuration_nodes(self, initialization: Initialization.Data):
        self._logger.debug(
            "%s: Configuring trigger configuration nodes.", self.dev_repr
        )
        nodes_to_configure_triggers = []

        dio_mode = initialization.config.dio_mode
        if dio_mode == DIOConfigType.ZSYNC_DIO:
            self._logger.debug(
                "%s: Configuring DIO mode: ZSync pass-through.", self.dev_repr
            )
            self._logger.debug(
                "%s: Configuring external clock to ZSync.", self.dev_repr
            )
            if self._daq.dataserver_version <= LabOneVersion.V_20_06:
                nodes_to_configure_triggers.append(
                    DaqNodeSetAction(self._daq, f"/{self.serial}/raw/dios/0/mode", 0x01)
                )
                nodes_to_configure_triggers.append(
                    DaqNodeSetAction(
                        self._daq, f"/{self.serial}/raw/dios/0/extclk", 0x1
                    )
                )
            else:
                nodes_to_configure_triggers.append(
                    DaqNodeSetAction(self._daq, f"/{self.serial}/dios/0/mode", 3)
                )

            nodes_to_configure_triggers.append(
                DaqNodeSetAction(self._daq, f"/{self.serial}/dios/0/drive", 0xC)
            )

            # Loop over at least AWG instance to cover the case that the instrument is only used as a communication proxy.
            # Some of the nodes on the AWG branch are needed to get proper communication between HDAWG and UHFQA.
            for awg_index in (
                self._allocated_awgs if len(self._allocated_awgs) > 0 else range(1)
            ):
                nodes_to_configure_triggers.append(
                    DaqNodeSetAction(
                        self._daq,
                        f"/{self.serial}/awgs/{awg_index}/dio/strobe/slope",
                        0,
                    )
                )
                nodes_to_configure_triggers.append(
                    DaqNodeSetAction(
                        self._daq,
                        f"/{self.serial}/awgs/{awg_index}/dio/valid/polarity",
                        2,
                    )
                )
                nodes_to_configure_triggers.append(
                    DaqNodeSetAction(
                        self._daq, f"/{self.serial}/awgs/{awg_index}/dio/valid/index", 0
                    )
                )
                nodes_to_configure_triggers.append(
                    DaqNodeSetAction(
                        self._daq,
                        f"/{self.serial}/awgs/{awg_index}/dio/mask/value",
                        0x3FF,
                    )
                )
                nodes_to_configure_triggers.append(
                    DaqNodeSetAction(
                        self._daq, f"/{self.serial}/awgs/{awg_index}/dio/mask/shift", 1
                    )
                )
        elif dio_mode == DIOConfigType.HDAWG_LEADER:

            nodes_to_configure_triggers.append(
                DaqNodeSetAction(
                    self._daq,
                    f"/{self.serial}/triggers/in/0/level",
                    DIG_TRIGGER_1_LEVEL,
                )
            )

            for awg_index in (
                self._allocated_awgs if len(self._allocated_awgs) > 0 else range(1)
            ):
                nodes_to_configure_triggers.append(
                    DaqNodeSetAction(
                        self._daq,
                        f"/{self.serial}/awgs/{awg_index}/auxtriggers/0/slope",
                        1,
                    )
                )
                nodes_to_configure_triggers.append(
                    DaqNodeSetAction(
                        self._daq,
                        f"/{self.serial}/awgs/{awg_index}/auxtriggers/0/channel",
                        0,
                    )
                )

            clock_source = initialization.config.reference_clock_source
            nodes_to_configure_triggers.append(
                DaqNodeSetAction(
                    self._daq,
                    f"/{self.serial}/system/clocks/referenceclock/source",
                    REFERENCE_CLOCK_SOURCE_INTERNAL
                    if clock_source
                    and clock_source.value == ReferenceClockSource.INTERNAL.value
                    else REFERENCE_CLOCK_SOURCE_EXTERNAL,
                )
            )
            nodes_to_configure_triggers.append(
                DaqNodeSetAction(self._daq, f"/{self.serial}/triggers/out/0/source", 4)
            )

            nodes_to_configure_triggers.append(
                DaqNodeSetAction(self._daq, f"/{self.serial}/triggers/out/1/source", 4)
            )

            nodes_to_configure_triggers.append(
                DaqNodeSetAction(self._daq, f"/{self.serial}/dios/0/mode", 1)
            )

            nodes_to_configure_triggers.append(
                DaqNodeSetAction(self._daq, f"/{self.serial}/dios/0/drive", 15)
            )

            # Loop over at least AWG instance to cover the case that the instrument is only used as a communication proxy.
            # Some of the nodes on the AWG branch are needed to get proper communication between HDAWG and UHFQA.
            for awg_index in (
                self._allocated_awgs if len(self._allocated_awgs) > 0 else range(1)
            ):

                nodes_to_configure_triggers.append(
                    DaqNodeSetAction(
                        self._daq,
                        f"/{self.serial}/awgs/{awg_index}/dio/strobe/slope",
                        0,
                    )
                )
                nodes_to_configure_triggers.append(
                    DaqNodeSetAction(
                        self._daq,
                        f"/{self.serial}/awgs/{awg_index}/dio/valid/polarity",
                        2,
                    )
                )
                nodes_to_configure_triggers.append(
                    DaqNodeSetAction(
                        self._daq, f"/{self.serial}/awgs/{awg_index}/dio/valid/index", 0
                    )
                )
                nodes_to_configure_triggers.append(
                    DaqNodeSetAction(
                        self._daq,
                        f"/{self.serial}/awgs/{awg_index}/dio/mask/value",
                        0x3FF,
                    )
                )
                nodes_to_configure_triggers.append(
                    DaqNodeSetAction(
                        self._daq, f"/{self.serial}/awgs/{awg_index}/dio/mask/shift", 1
                    )
                )

        return nodes_to_configure_triggers

    def configure_as_leader(self, initialization):
        count = 1
        while True:

            source_path = f"/{self.serial}/system/clocks/referenceclock/source"
            status_path = f"/{self.serial}/system/clocks/referenceclock/status"

            daq_reply = self._daq.batch_get(
                [
                    DaqNodeGetAction(
                        self._daq,
                        source_path,
                        caching_strategy=CachingStrategy.NO_CACHE,
                    ),
                    DaqNodeGetAction(
                        self._daq,
                        status_path,
                        caching_strategy=CachingStrategy.NO_CACHE,
                    ),
                ]
            )

            refclock_source = daq_reply[source_path]
            refclock_status = daq_reply[status_path]

            if refclock_source == 1 and refclock_status == 0:

                refclock_freq_path = f"/{self.serial}/system/clocks/referenceclock/freq"

                daq_reply = self._daq.batch_get(
                    [
                        DaqNodeGetAction(
                            self._daq,
                            refclock_freq_path,
                            caching_strategy=CachingStrategy.NO_CACHE,
                        )
                    ]
                )

                refclock_freq = daq_reply[refclock_freq_path]

                if refclock_freq == 10e6:
                    self._logger.debug(
                        "HDAWG:%s: successfully locked to external clock on the %d time.",
                        self.serial,
                        count,
                    )
                    break
                else:
                    raise LabOneQControllerException(
                        f"HDAWG:{self.serial}: unable to lock to external clock.\n "
                    )

            if self.dry_run:
                break

            if refclock_status == 2 and count < 20:
                self._logger.debug(
                    "HDAWG:%s: Trying to lock to external clock for the %d time...",
                    self.serial,
                    count,
                )
            elif count >= 20:
                raise LabOneQControllerException(
                    f"HDAWG:{self.serial}: unable to lock to external clock.\n "
                )
            else:
                if refclock_status == 1:
                    self._logger.debug("/Unable to lock to external clock...retrying")
                clock_source = initialization.config.reference_clock_source
                self._daq.batch_set(
                    [
                        DaqNodeSetAction(
                            self._daq,
                            f"/{self.serial}/system/clocks/referenceclock/source",
                            REFERENCE_CLOCK_SOURCE_INTERNAL
                            if clock_source
                            and clock_source.value
                            == ReferenceClockSource.INTERNAL.value
                            else REFERENCE_CLOCK_SOURCE_EXTERNAL,
                            caching_strategy=CachingStrategy.NO_CACHE,
                        )
                    ]
                )
            count += 1

            time.sleep(0.1)

    def collect_follower_configuration_nodes(self, initialization):
        dio_mode = initialization.config.dio_mode
        self._logger.debug("%s: Configuring as a follower...", self.dev_repr)

        nodes_to_configure_as_follower = []
        if dio_mode == DIOConfigType.ZSYNC_DIO:
            self._logger.debug(
                "%s: Configuring reference clock to use ZSYNC as a reference...",
                self.dev_repr,
            )
            nodes_to_configure_as_follower.append(
                DaqNodeSetAction(
                    self._daq, f"/{self.serial}/system/clocks/referenceclock/source", 2
                )
            )
        elif dio_mode == DIOConfigType.HDAWG_LEADER:
            pass
        else:
            raise LabOneQControllerException(
                f"{self.dev_repr}: Unsupported DIO mode {dio_mode} for device type: HDAWG."
            )

        return nodes_to_configure_as_follower

    def initialize_sweep_setting(self, setting):
        raise LabOneQControllerException("HDAWG doesn't support sweeping")

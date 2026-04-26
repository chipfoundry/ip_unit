"""Test library for CF_I2S verification — 8 tests covering I2S receive functionality."""

import os
from pathlib import Path

import cocotb
import pyuvm
from pyuvm import ConfigDB, uvm_root

from cocotb.triggers import ClockCycles
from cocotb_coverage.coverage import coverage_db

from cf_verify.base.base_test import base_test
from cf_verify.base.top_env import top_env
from cf_verify.bus_env.bus_regs import BusRegs
from cf_verify.bus_env.bus_seq_lib import (
    write_read_regs_seq,
    reset_seq,
    write_reg_seq,
    read_reg_seq,
)
from cf_verify.ip_env.ip_agent import ip_agent
from cf_verify.ip_env.ip_driver import ip_driver
from cf_verify.ip_env.ip_monitor import ip_monitor
from cf_verify.ip_env.ip_coverage import ip_coverage

from ip_agent.i2s_driver import i2s_driver
from ip_agent.i2s_monitor import i2s_monitor
from ip_coverage.i2s_coverage import i2s_coverage
from ip_scoreboard import i2s_scoreboard


class i2s_env(top_env):
    """I2S-specific top environment with proper component wiring."""

    def build_phase(self):
        from cf_verify.bus_env.bus_agent import bus_agent
        from cf_verify.ip_env.ip_logger import ip_logger
        from cf_verify.base.ref_model import ref_model

        self.bus_agent = bus_agent("bus_agent", self)
        self.ip_agent = i2s_ip_agent("ip_agent", self)
        self.ref_model = ref_model("ref_model", self)
        self.scoreboard = i2s_scoreboard("scoreboard", self)
        self.ip_coverage = i2s_coverage("ip_coverage", self)
        self.ip_logger = ip_logger("ip_logger", self)

    def connect_phase(self):
        super().connect_phase()
        self.bus_agent.monitor.ap.connect(self.ip_coverage.analysis_export)


class i2s_ip_agent(ip_agent):
    driver_cls = i2s_driver
    monitor_cls = i2s_monitor


class i2s_base_test(base_test):
    """Base test for CF_I2S — wires up the I2S environment."""

    def build_phase(self):
        import os
        import cocotb

        dut = cocotb.top
        bus_type = os.environ.get("BUS_TYPE", "APB")
        yaml_file = os.environ.get(
            "YAML_FILE",
            str(Path(__file__).resolve().parent.parent.parent / "CF_I2S.yaml"),
        )
        test_path = os.environ.get("TEST_PATH", "./sim")

        regs = BusRegs(yaml_file)

        ConfigDB().set(None, "*", "DUT", dut)
        ConfigDB().set(None, "*", "BUS_TYPE", bus_type)
        ConfigDB().set(None, "*", "bus_regs", regs)
        ConfigDB().set(None, "*", "irq_exist", regs.get_irq_exist())
        ConfigDB().set(None, "*", "collect_coverage", True)
        ConfigDB().set(None, "*", "disable_logger", False)
        ConfigDB().set(None, "*", "TEST_PATH", test_path)

        self.env = i2s_env("env", self)
        super().build_phase()


# ──────────────────────────────────────────
#  I2S TESTS
# ──────────────────────────────────────────

@pyuvm.test()
class WriteReadRegsTest(i2s_base_test):
    """Write/read all accessible registers."""

    async def run_phase(self):
        self.raise_objection()
        seq = write_read_regs_seq("write_read_regs")
        await seq.start(self.env.bus_agent.sequencer)

        regs = ConfigDB().get(None, "", "bus_regs")
        addr = regs.reg_name_to_address
        for reg in regs.get_writable_regs():
            if reg.name in ("IC", "GCLK") or reg.name.endswith("_FLUSH"):
                continue
            if reg.mode == "w":
                continue
            wr_val = (
                0xA5 if reg.size <= 8
                else 0xA5A5 if reg.size <= 16
                else 0xDEAD_BEEF
            ) & ((1 << reg.size) - 1)
            await write_reg_seq("wr_chk", addr[reg.name], wr_val).start(
                self.env.bus_agent.sequencer
            )
            rd = read_reg_seq("rd_chk", addr[reg.name])
            await rd.start(self.env.bus_agent.sequencer)
            rd_val = rd.result & ((1 << reg.size) - 1)
            assert rd_val == wr_val, (
                f"WriteReadRegsTest mismatch on {reg.name}: "
                f"wrote 0x{wr_val:x}, read 0x{rd_val:x}"
            )
        self.drop_objection()


@pyuvm.test()
class LeftChannelTest(i2s_base_test):
    """Left channel — receive left-channel-only audio."""

    async def run_phase(self):
        self.raise_objection()
        from seq_lib.i2s_channel_seq import i2s_left_channel_seq
        seq = i2s_left_channel_seq("left_ch")
        await seq.start(self.env.bus_agent.sequencer)
        self.drop_objection()


@pyuvm.test()
class RightChannelTest(i2s_base_test):
    """Right channel — receive right-channel-only audio."""

    async def run_phase(self):
        self.raise_objection()
        from seq_lib.i2s_channel_seq import i2s_right_channel_seq
        seq = i2s_right_channel_seq("right_ch")
        await seq.start(self.env.bus_agent.sequencer)
        self.drop_objection()


@pyuvm.test()
class StereoTest(i2s_base_test):
    """Stereo — receive both left and right channels."""

    async def run_phase(self):
        self.raise_objection()
        from seq_lib.i2s_channel_seq import i2s_stereo_seq
        seq = i2s_stereo_seq("stereo")
        await seq.start(self.env.bus_agent.sequencer)
        self.drop_objection()


@pyuvm.test()
class PrescalerTest(i2s_base_test):
    """Prescaler — tests different sample rates via prescaler sweep."""

    async def run_phase(self):
        self.raise_objection()
        from seq_lib.i2s_receive_seq import i2s_receive_seq
        dut = ConfigDB().get(self, "", "DUT")

        for pr in [2, 4, 8, 16]:
            seq = i2s_receive_seq(
                f"rx_pr{pr}", prescaler=pr,
                channels=3, sample_size=16, num_samples=2,
            )
            await seq.start(self.env.bus_agent.sequencer)

        self.drop_objection()


@pyuvm.test()
class FIFOTest(i2s_base_test):
    """FIFO — tests FIFO full, empty, threshold, and flush."""

    async def run_phase(self):
        self.raise_objection()
        from seq_lib.i2s_fifo_seq import i2s_fifo_seq
        seq = i2s_fifo_seq("fifo_test")
        await seq.start(self.env.bus_agent.sequencer)
        self.drop_objection()


@pyuvm.test()
class InterruptTest(i2s_base_test):
    """Interrupt — verifies all interrupt sources fire and clear correctly."""

    async def run_phase(self):
        self.raise_objection()
        from seq_lib.i2s_interrupt_seq import i2s_interrupt_seq
        seq = i2s_interrupt_seq("irq_test")
        await seq.start(self.env.bus_agent.sequencer)
        self.drop_objection()


@pyuvm.test()
class SampleSizeTest(i2s_base_test):
    """Sample size — tests different sample sizes (8, 16, 24, 32 bit)."""

    async def run_phase(self):
        self.raise_objection()
        from seq_lib.i2s_receive_seq import i2s_receive_seq
        dut = ConfigDB().get(self, "", "DUT")

        for ss in [8, 16, 24, 32]:
            seq = i2s_receive_seq(
                f"rx_ss{ss}", prescaler=4,
                channels=3, sample_size=ss, num_samples=2,
            )
            await seq.start(self.env.bus_agent.sequencer)

        self.drop_objection()


@pyuvm.test()
class CoverageClosureTest(i2s_base_test):
    """Coverage closure — systematically exercises all coverage bins."""

    async def run_phase(self):
        self.raise_objection()
        from seq_lib.i2s_coverage_closure_seq import i2s_coverage_closure_seq
        seq = i2s_coverage_closure_seq("cov_closure")
        await seq.start(self.env.bus_agent.sequencer)
        self.drop_objection()

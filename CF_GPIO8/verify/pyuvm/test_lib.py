"""Test library for CF_GPIO8 verification — 7 tests covering full GPIO functionality."""

import os
from pathlib import Path

import cocotb
import pyuvm
from pyuvm import uvm_root, ConfigDB

from cocotb.triggers import ClockCycles
from cocotb_coverage.coverage import coverage_db

from cf_verify.base.base_test import base_test
from cf_verify.base.top_env import top_env
from cf_verify.bus_env.bus_regs import BusRegs
from cf_verify.bus_env.bus_seq_lib import write_read_regs_seq, reset_seq
from cf_verify.ip_env.ip_agent import ip_agent
from cf_verify.ip_env.ip_driver import ip_driver
from cf_verify.ip_env.ip_monitor import ip_monitor
from cf_verify.ip_env.ip_coverage import ip_coverage

from ip_agent.gpio_driver import gpio_driver
from ip_agent.gpio_monitor import gpio_monitor
from ip_coverage.gpio_coverage import gpio_coverage
from ip_scoreboard import gpio_scoreboard


class gpio_env(top_env):
    """GPIO-specific top environment with proper component wiring."""

    def build_phase(self):
        from cf_verify.bus_env.bus_agent import bus_agent
        from cf_verify.ip_env.ip_logger import ip_logger
        from cf_verify.base.ref_model import ref_model

        self.bus_agent = bus_agent("bus_agent", self)
        self.ip_agent = gpio_ip_agent("ip_agent", self)
        self.ref_model = ref_model("ref_model", self)
        self.scoreboard = gpio_scoreboard("scoreboard", self)
        self.ip_coverage = gpio_coverage("ip_coverage", self)
        self.ip_logger = ip_logger("ip_logger", self)

    def connect_phase(self):
        super().connect_phase()
        self.bus_agent.monitor.ap.connect(self.ip_coverage.analysis_export)


class gpio_ip_agent(ip_agent):
    driver_cls = gpio_driver
    monitor_cls = gpio_monitor


class gpio_base_test(base_test):
    """Base test for CF_GPIO8 — wires up the GPIO environment."""

    def build_phase(self):
        import os
        import cocotb

        dut = cocotb.top
        bus_type = os.environ.get("BUS_TYPE", "APB")
        yaml_file = os.environ.get(
            "YAML_FILE",
            str(Path(__file__).resolve().parent.parent.parent / "CF_GPIO8.yaml"),
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

        self.env = gpio_env("env", self)
        super().build_phase()


# ──────────────────────────────────────────
#  7 GPIO TESTS
# ──────────────────────────────────────────

@pyuvm.test()
class WriteReadRegsTest(gpio_base_test):
    """Write/read all accessible registers."""

    async def run_phase(self):
        from cf_verify.bus_env.bus_seq_lib import write_reg_seq, read_reg_seq

        self.raise_objection()
        seq = write_read_regs_seq("write_read_regs")
        await seq.start(self.env.bus_agent.sequencer)

        regs = ConfigDB().get(None, "", "bus_regs")
        addr = regs.reg_name_to_address
        for reg in regs.get_writable_regs():
            if reg.name in ("IC", "GCLK") or reg.name.endswith("_FLUSH"):
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
class OutputTest(gpio_base_test):
    """Output — sets all pins as output and writes various data patterns."""

    async def run_phase(self):
        self.raise_objection()
        from seq_lib.gpio_output_seq import gpio_output_seq
        seq = gpio_output_seq("output_test")
        await seq.start(self.env.bus_agent.sequencer)
        self.drop_objection()


@pyuvm.test()
class InputTest(gpio_base_test):
    """Input — sets all pins as input, drives io_in, reads DATAI."""

    async def run_phase(self):
        self.raise_objection()
        from seq_lib.gpio_input_seq import gpio_input_seq
        seq = gpio_input_seq("input_test")
        await seq.start(self.env.bus_agent.sequencer)
        self.drop_objection()


@pyuvm.test()
class DirectionTest(gpio_base_test):
    """Direction — tests all direction register combinations."""

    async def run_phase(self):
        self.raise_objection()
        from seq_lib.gpio_direction_seq import gpio_direction_seq
        seq = gpio_direction_seq("direction_test")
        await seq.start(self.env.bus_agent.sequencer)
        self.drop_objection()


@pyuvm.test()
class EdgeDetectTest(gpio_base_test):
    """Edge detect — verifies positive and negative edge flags per pin."""

    async def run_phase(self):
        self.raise_objection()
        from seq_lib.gpio_edge_detect_seq import gpio_edge_detect_seq
        seq = gpio_edge_detect_seq("edge_detect_test")
        await seq.start(self.env.bus_agent.sequencer)
        self.drop_objection()


@pyuvm.test()
class InterruptTest(gpio_base_test):
    """Interrupt — verifies all 32 interrupt sources fire and clear correctly."""

    async def run_phase(self):
        self.raise_objection()
        from seq_lib.gpio_interrupt_seq import gpio_interrupt_seq
        seq = gpio_interrupt_seq("irq_test")
        await seq.start(self.env.bus_agent.sequencer)
        self.drop_objection()


@pyuvm.test()
class CoverageClosureTest(gpio_base_test):
    """Coverage closure — systematically exercises all coverage bins."""

    async def run_phase(self):
        self.raise_objection()
        from seq_lib.gpio_coverage_closure_seq import gpio_coverage_closure_seq
        seq = gpio_coverage_closure_seq("cov_closure")
        await seq.start(self.env.bus_agent.sequencer)
        self.drop_objection()

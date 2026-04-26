"""Test library for CF_WDT32 verification — 6 tests covering full WDT functionality."""

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

from ip_agent.wdt_driver import wdt_driver
from ip_agent.wdt_monitor import wdt_monitor
from ip_coverage.wdt_coverage import wdt_coverage
from ip_scoreboard import wdt_scoreboard


class wdt_env(top_env):
    """WDT-specific top environment with proper component wiring."""

    def build_phase(self):
        from cf_verify.bus_env.bus_agent import bus_agent
        from cf_verify.ip_env.ip_logger import ip_logger
        from cf_verify.base.ref_model import ref_model

        self.bus_agent = bus_agent("bus_agent", self)
        self.ip_agent = wdt_ip_agent("ip_agent", self)
        self.ref_model = ref_model("ref_model", self)
        self.scoreboard = wdt_scoreboard("scoreboard", self)
        self.ip_coverage = wdt_coverage("ip_coverage", self)
        self.ip_logger = ip_logger("ip_logger", self)

    def connect_phase(self):
        super().connect_phase()
        self.bus_agent.monitor.ap.connect(self.ip_coverage.analysis_export)


class wdt_ip_agent(ip_agent):
    driver_cls = wdt_driver
    monitor_cls = wdt_monitor


class wdt_base_test(base_test):
    """Base test for CF_WDT32 — wires up the WDT environment."""

    def build_phase(self):
        import os
        import cocotb

        dut = cocotb.top
        bus_type = os.environ.get("BUS_TYPE", "APB")
        yaml_file = os.environ.get(
            "YAML_FILE",
            str(Path(__file__).resolve().parent.parent.parent / "CF_WDT32.yaml"),
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

        self.env = wdt_env("env", self)
        super().build_phase()


# ──────────────────────────────────────────
#  6 WDT TESTS
# ──────────────────────────────────────────

@pyuvm.test()
class WriteReadRegsTest(wdt_base_test):
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
            # Core WDT `load` / `control` are write-only; readback is not defined.
            if getattr(reg, "mode", "") == "w":
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
class EnableDisableTest(wdt_base_test):
    """Tests enabling and disabling the WDT and verifying counter behavior."""

    async def run_phase(self):
        self.raise_objection()
        from cf_verify.bus_env.bus_seq_lib import write_reg_seq, read_reg_seq

        regs = ConfigDB().get(None, "", "bus_regs")
        addr = regs.reg_name_to_address
        dut = ConfigDB().get(self, "", "DUT")

        if "GCLK" in addr:
            await write_reg_seq("gclk", addr["GCLK"], 1).start(
                self.env.bus_agent.sequencer
            )

        await write_reg_seq("load", addr["load"], 0x100).start(
            self.env.bus_agent.sequencer
        )

        await write_reg_seq("ctrl_on", addr["control"], 1).start(
            self.env.bus_agent.sequencer
        )
        await ClockCycles(dut.CLK, 20)
        await read_reg_seq("rd_timer1", addr["timer"]).start(
            self.env.bus_agent.sequencer
        )

        await write_reg_seq("ctrl_off", addr["control"], 0).start(
            self.env.bus_agent.sequencer
        )
        await ClockCycles(dut.CLK, 10)
        await read_reg_seq("rd_timer2", addr["timer"]).start(
            self.env.bus_agent.sequencer
        )

        await write_reg_seq("ctrl_on2", addr["control"], 1).start(
            self.env.bus_agent.sequencer
        )
        await ClockCycles(dut.CLK, 10)
        await read_reg_seq("rd_timer3", addr["timer"]).start(
            self.env.bus_agent.sequencer
        )

        await write_reg_seq("ctrl_off2", addr["control"], 0).start(
            self.env.bus_agent.sequencer
        )
        self.drop_objection()


@pyuvm.test()
class TimeoutTest(wdt_base_test):
    """Enables WDT with small load value, waits for timeout, verifies flag."""

    async def run_phase(self):
        self.raise_objection()
        from seq_lib.wdt_timeout_seq import wdt_timeout_seq
        seq = wdt_timeout_seq("timeout_test", load_value=0x10)
        await seq.start(self.env.bus_agent.sequencer)
        self.drop_objection()


@pyuvm.test()
class ReloadTest(wdt_base_test):
    """Tests reload behavior by changing load value mid-countdown."""

    async def run_phase(self):
        self.raise_objection()
        from seq_lib.wdt_reload_seq import wdt_reload_seq
        seq = wdt_reload_seq("reload_test")
        await seq.start(self.env.bus_agent.sequencer)
        self.drop_objection()


@pyuvm.test()
class InterruptTest(wdt_base_test):
    """Verifies interrupt mask, status, and clear register behavior."""

    async def run_phase(self):
        self.raise_objection()
        from seq_lib.wdt_interrupt_seq import wdt_interrupt_seq
        seq = wdt_interrupt_seq("irq_test")
        await seq.start(self.env.bus_agent.sequencer)
        self.drop_objection()


@pyuvm.test()
class CoverageClosureTest(wdt_base_test):
    """Coverage closure — systematically exercises all coverage bins."""

    async def run_phase(self):
        self.raise_objection()
        from seq_lib.wdt_coverage_closure_seq import wdt_coverage_closure_seq
        seq = wdt_coverage_closure_seq("cov_closure")
        await seq.start(self.env.bus_agent.sequencer)
        self.drop_objection()

"""Test library for CF_USB_CDC_WRAPPER verification — 6 register/FIFO-level tests.

Note: Without a full USB host model, protocol-level verification is limited.
These tests focus on register access, FIFO behavior, thresholds, and interrupts.
"""

import os
from pathlib import Path

import cocotb
import pyuvm
from pyuvm import ConfigDB, uvm_root

from cocotb.triggers import Event
from cocotb_coverage.coverage import coverage_db

from cf_verify.base.base_test import base_test
from cf_verify.base.top_env import top_env
from cf_verify.bus_env.bus_regs import BusRegs
from cocotb.triggers import ClockCycles

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

from ip_agent.usb_driver import usb_driver
from ip_agent.usb_monitor import usb_monitor
from ip_coverage.usb_coverage import usb_coverage
from ip_scoreboard import usb_scoreboard


class usb_env(top_env):
    """USB CDC-specific top environment."""

    def build_phase(self):
        from cf_verify.bus_env.bus_agent import bus_agent
        from cf_verify.ip_env.ip_logger import ip_logger
        from cf_verify.base.ref_model import ref_model

        self.bus_agent = bus_agent("bus_agent", self)
        self.ip_agent = usb_ip_agent("ip_agent", self)
        self.ref_model = ref_model("ref_model", self)
        self.scoreboard = usb_scoreboard("scoreboard", self)
        self.ip_coverage = usb_coverage("ip_coverage", self)
        self.ip_logger = ip_logger("ip_logger", self)

    def connect_phase(self):
        super().connect_phase()
        self.bus_agent.monitor.ap.connect(self.ip_coverage.analysis_export)


class usb_ip_agent(ip_agent):
    driver_cls = usb_driver
    monitor_cls = usb_monitor


class usb_base_test(base_test):
    """Base test for CF_USB_CDC_WRAPPER — wires up the USB environment."""

    def build_phase(self):
        import os
        import cocotb

        dut = cocotb.top
        bus_type = os.environ.get("BUS_TYPE", "APB")
        yaml_file = os.environ.get(
            "YAML_FILE",
            str(Path(__file__).resolve().parent.parent.parent / "CF_USB_CDC_WRAPPER.yaml"),
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

        self.env = usb_env("env", self)
        super().build_phase()


# ──────────────────────────────────────────
#  Register & FIFO Tests
# ──────────────────────────────────────────

@pyuvm.test()
class WriteReadRegsTest(usb_base_test):
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
class UsbPhySmokeTest(usb_base_test):
    """PHY smoke — after reset, pad-related outputs are defined (replaces legacy Verilog loopback TB sanity).

    Full USB enumeration and bulk transfer are not replicated here; those require a host BFM.
    This test only ensures the wrapper leaves reset with resolvable PHY outputs.
    """

    async def run_phase(self):
        self.raise_objection()
        await reset_seq("rst").start(self.env.bus_agent.sequencer)
        dut = ConfigDB().get(self, "", "DUT")
        await ClockCycles(dut.CLK, 200)
        for name in ("dp_pu_o", "dp_tx_o", "dn_tx_o", "tx_en_o"):
            sig = getattr(dut, name, None)
            assert sig is not None, f"DUT missing {name}"
            v = sig.value
            assert v.is_resolvable, f"{name} is X/Z after reset"
            assert int(v) in (0, 1), f"{name} invalid: {v}"
        self.drop_objection()


@pyuvm.test()
class TXFIFOTest(usb_base_test):
    """TX FIFO — fills FIFO, checks level and overflow behavior."""

    async def run_phase(self):
        self.raise_objection()
        from seq_lib.usb_fifo_seq import usb_tx_fifo_seq
        seq = usb_tx_fifo_seq("tx_fifo_test")
        await seq.start(self.env.bus_agent.sequencer)
        self.drop_objection()


@pyuvm.test()
class RXFIFOTest(usb_base_test):
    """RX FIFO — reads from empty FIFO, checks empty flag."""

    async def run_phase(self):
        self.raise_objection()
        from seq_lib.usb_fifo_seq import usb_rx_fifo_seq
        seq = usb_rx_fifo_seq("rx_fifo_test")
        await seq.start(self.env.bus_agent.sequencer)
        self.drop_objection()


@pyuvm.test()
class ThresholdTest(usb_base_test):
    """Threshold — verifies TX/RX FIFO threshold configuration and flags."""

    async def run_phase(self):
        self.raise_objection()
        from seq_lib.usb_threshold_seq import usb_threshold_seq
        seq = usb_threshold_seq("threshold_test")
        await seq.start(self.env.bus_agent.sequencer)
        self.drop_objection()


@pyuvm.test()
class InterruptTest(usb_base_test):
    """Interrupt — verifies all interrupt sources fire and clear correctly."""

    async def run_phase(self):
        self.raise_objection()
        from seq_lib.usb_interrupt_seq import usb_interrupt_seq
        seq = usb_interrupt_seq("irq_test")
        await seq.start(self.env.bus_agent.sequencer)
        self.drop_objection()


@pyuvm.test()
class CoverageClosureTest(usb_base_test):
    """Coverage closure — systematically hits all remaining coverage bins."""

    async def run_phase(self):
        self.raise_objection()
        from seq_lib.usb_coverage_closure_seq import usb_coverage_closure_seq
        seq = usb_coverage_closure_seq("cov_closure")
        await seq.start(self.env.bus_agent.sequencer)
        self.drop_objection()

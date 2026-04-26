"""Test library for CF_QSPI_XIP_CTRL verification.

This IP has NO registers — it is a pure memory-mapped QSPI flash cache controller.
Standard register-based verification (WriteReadRegsTest) does not apply.
Tests focus on: compilation, reset behavior, and flash read via AHB.
"""

import os
from pathlib import Path

import cocotb
import pyuvm
from pyuvm import uvm_root, ConfigDB

from cocotb.triggers import ClockCycles, RisingEdge, Timer
from cocotb_coverage.coverage import coverage_db

from cf_verify.base.base_test import base_test
from cf_verify.base.top_env import top_env
from cf_verify.ip_env.ip_agent import ip_agent
from cf_verify.ip_env.ip_driver import ip_driver
from cf_verify.ip_env.ip_monitor import ip_monitor
from cf_verify.ip_env.ip_coverage import ip_coverage
from cf_verify.base.ref_model import ref_model

from ip_agent.qspi_driver import qspi_driver
from ip_agent.qspi_monitor import qspi_monitor
from ref_model.ref_model import QSPI_VIP
from ip_coverage.qspi_coverage import qspi_coverage
from ip_scoreboard import qspi_scoreboard


class qspi_env(top_env):
    """QSPI-specific top environment."""

    def build_phase(self):
        from cf_verify.bus_env.bus_agent import bus_agent
        from cf_verify.ip_env.ip_logger import ip_logger

        self.bus_agent = bus_agent("bus_agent", self)
        self.ip_agent = qspi_ip_agent("ip_agent", self)
        self.ref_model = QSPI_VIP("ref_model", self)
        self.scoreboard = qspi_scoreboard("scoreboard", self)
        self.ip_coverage = qspi_coverage("ip_coverage", self)
        self.ip_logger = ip_logger("ip_logger", self)

    def connect_phase(self):
        super().connect_phase()
        self.bus_agent.monitor.ap.connect(self.ip_coverage.analysis_export)


class qspi_ip_agent(ip_agent):
    driver_cls = qspi_driver
    monitor_cls = qspi_monitor


class qspi_base_test(base_test):
    """Base test for CF_QSPI_XIP_CTRL."""

    def build_phase(self):
        dut = cocotb.top
        bus_type = os.environ.get("BUS_TYPE", "AHB")
        yaml_file = os.environ.get(
            "YAML_FILE",
            str(Path(__file__).resolve().parent.parent.parent / "CF_QSPI_XIP_CTRL.yaml"),
        )
        test_path = os.environ.get("TEST_PATH", "./sim")

        from cf_verify.bus_env.bus_regs import BusRegs
        regs = BusRegs(yaml_file)

        ConfigDB().set(None, "*", "DUT", dut)
        ConfigDB().set(None, "*", "BUS_TYPE", bus_type)
        ConfigDB().set(None, "*", "bus_regs", regs)
        ConfigDB().set(None, "*", "irq_exist", regs.get_irq_exist())
        ConfigDB().set(None, "*", "collect_coverage", True)
        ConfigDB().set(None, "*", "disable_logger", False)
        ConfigDB().set(None, "*", "TEST_PATH", test_path)

        memory_size = 0x100000
        flash_memory = os.urandom(memory_size)
        ConfigDB().set(None, "*", "flash_memory", flash_memory)
        ConfigDB().set(None, "*", "flash_size", memory_size)

        self.env = qspi_env("env", self)
        super().build_phase()

    async def _load_flash_vip(self):
        """Load random data into the SST26WF080B VIP memory."""
        dut = ConfigDB().get(self, "", "DUT")
        flash_memory = ConfigDB().get(None, "", "flash_memory")
        try:
            for i in range(len(flash_memory)):
                dut.vip.I0.memory[i].value = flash_memory[i]
            self.logger.info(f"Loaded {len(flash_memory)} bytes into flash VIP")
        except AttributeError:
            self.logger.warning("Cannot access flash VIP memory hierarchy")

    async def _wait_reset_done(self):
        """Wait for the controller's flash reset sequence to complete.
        The controller issues a software reset (0x66/0x99) after HRESETn deasserts.
        This takes ~2*(RESET_CYCLES+1) clock cycles (default RESET_CYCLES=999 -> ~2000 clks).
        """
        dut = ConfigDB().get(self, "", "DUT")
        await RisingEdge(dut.RESETn)
        await ClockCycles(dut.CLK, 2200)


# ──────────────────────────────────────────
#  TESTS
# ──────────────────────────────────────────

@pyuvm.test()
class CompilationTest(qspi_base_test):
    """Verify RTL compiles and the simulation can start.
    This is the most fundamental test — if compilation fails, nothing else works.
    """

    async def run_phase(self):
        self.raise_objection()
        dut = ConfigDB().get(self, "", "DUT")
        await RisingEdge(dut.RESETn)
        await ClockCycles(dut.CLK, 10)
        self.logger.info("CompilationTest: RTL compiled and simulated successfully")
        self.drop_objection()


@pyuvm.test()
class ResetDeassertionTest(qspi_base_test):
    """Verify the controller completes its flash reset sequence after HRESETn.
    After reset deasserts, the controller sends 0x66 (Reset Enable) and 0x99
    (Reset Memory) commands. HREADYOUT should return to 1 after the sequence.
    """

    async def run_phase(self):
        self.raise_objection()
        dut = ConfigDB().get(self, "", "DUT")

        await RisingEdge(dut.RESETn)
        self.logger.info("Reset deasserted — waiting for flash reset sequence")

        await ClockCycles(dut.CLK, 2200)

        hreadyout = int(dut.HREADYOUT.value)
        assert hreadyout == 1, (
            f"HREADYOUT={hreadyout} after reset sequence — expected 1"
        )
        self.logger.info("HREADYOUT=1 after reset — controller is ready")

        ce_n = int(dut.ce_n.value)
        assert ce_n == 1, (
            f"ce_n={ce_n} after reset — expected 1 (deasserted)"
        )
        self.logger.info("ce_n=1 — flash chip select deasserted after reset")

        self.drop_objection()


@pyuvm.test()
class FlashReadTest(qspi_base_test):
    """Read data from flash through the AHB interface.
    Loads random data into the SST26WF080B VIP memory, then issues AHB reads
    and verifies the returned data matches.
    """

    async def run_phase(self):
        self.raise_objection()
        await self._load_flash_vip()
        await self._wait_reset_done()

        from seq_lib.qspi_read_seq import qspi_read_seq
        flash_size = ConfigDB().get(None, "", "flash_size")
        seq = qspi_read_seq("flash_read", memory_size=flash_size)
        await seq.start(self.env.bus_agent.sequencer)

        dut = ConfigDB().get(self, "", "DUT")
        await ClockCycles(dut.CLK, 500)

        self.drop_objection()


@pyuvm.test()
class CacheMissReadTest(qspi_base_test):
    """Exercise cache miss paths by reading distinct cache lines.
    Each new line address forces a flash read transaction.
    """

    async def run_phase(self):
        self.raise_objection()
        await self._load_flash_vip()
        await self._wait_reset_done()

        from seq_lib.qspi_cache_seq import qspi_cache_miss_seq
        flash_size = ConfigDB().get(None, "", "flash_size")
        seq = qspi_cache_miss_seq("cache_miss", memory_size=flash_size)
        await seq.start(self.env.bus_agent.sequencer)

        dut = ConfigDB().get(self, "", "DUT")
        await ClockCycles(dut.CLK, 500)

        flash_accesses = self.env.ip_agent.monitor.flash_access_count
        self.logger.info(
            f"Flash access count after cache miss test: {flash_accesses}"
        )

        self.drop_objection()


@pyuvm.test()
class SequentialReadTest(qspi_base_test):
    """Read sequential addresses to test cache line reuse.
    The second pass over the same addresses should hit the cache.
    """

    async def run_phase(self):
        self.raise_objection()
        await self._load_flash_vip()
        await self._wait_reset_done()

        from seq_lib.qspi_cache_seq import qspi_sequential_read_seq
        flash_size = ConfigDB().get(None, "", "flash_size")
        seq = qspi_sequential_read_seq("seq_read", memory_size=flash_size)
        await seq.start(self.env.bus_agent.sequencer)

        dut = ConfigDB().get(self, "", "DUT")
        await ClockCycles(dut.CLK, 500)

        self.drop_objection()

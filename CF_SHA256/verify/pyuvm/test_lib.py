"""Test library for CF_SHA256 verification."""

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

from ip_agent.sha256_driver import sha256_driver
from ip_agent.sha256_monitor import sha256_monitor
from ip_coverage.sha256_coverage import sha256_coverage
from ip_scoreboard import sha256_scoreboard


class sha256_env(top_env):
    def build_phase(self):
        from cf_verify.bus_env.bus_agent import bus_agent
        from cf_verify.ip_env.ip_logger import ip_logger
        from cf_verify.base.ref_model import ref_model

        self.bus_agent = bus_agent("bus_agent", self)
        self.ip_agent = sha256_ip_agent("ip_agent", self)
        self.ref_model = ref_model("ref_model", self)
        self.scoreboard = sha256_scoreboard("scoreboard", self)
        self.ip_coverage = sha256_coverage("ip_coverage", self)
        self.ip_logger = ip_logger("ip_logger", self)

    def connect_phase(self):
        super().connect_phase()
        self.bus_agent.monitor.ap.connect(self.ip_coverage.analysis_export)


class sha256_ip_agent(ip_agent):
    driver_cls = sha256_driver
    monitor_cls = sha256_monitor


class sha256_base_test(base_test):
    def build_phase(self):
        dut = cocotb.top
        bus_type = os.environ.get("BUS_TYPE", "APB")
        yaml_file = os.environ.get(
            "YAML_FILE",
            str(Path(__file__).resolve().parent.parent.parent / "CF_SHA256.yaml"),
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

        self.env = sha256_env("env", self)
        super().build_phase()


@pyuvm.test()
class WriteReadRegsTest(sha256_base_test):
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
class SHA256SingleBlockTest(sha256_base_test):
    """SHA-256 single-block hash with NIST test vector."""

    async def run_phase(self):
        self.raise_objection()
        from seq_lib.sha256_single_block_seq import sha256_single_block_seq
        seq = sha256_single_block_seq("sha256_single")
        await seq.start(self.env.bus_agent.sequencer)
        self.drop_objection()


@pyuvm.test()
class SHA224SingleBlockTest(sha256_base_test):
    """SHA-224 single-block hash with NIST test vector."""

    async def run_phase(self):
        self.raise_objection()
        from seq_lib.sha224_single_block_seq import sha224_single_block_seq
        seq = sha224_single_block_seq("sha224_single")
        await seq.start(self.env.bus_agent.sequencer)
        self.drop_objection()


@pyuvm.test()
class SHA256MultiBlockTest(sha256_base_test):
    """SHA-256 multi-block hash — exercises init+next chaining."""

    async def run_phase(self):
        self.raise_objection()
        from seq_lib.sha256_multi_block_seq import sha256_multi_block_seq
        seq = sha256_multi_block_seq("sha256_multi")
        await seq.start(self.env.bus_agent.sequencer)
        self.drop_objection()


@pyuvm.test()
class InterruptTest(sha256_base_test):
    """Interrupt — verifies valid and ready interrupt sources."""

    async def run_phase(self):
        self.raise_objection()
        from seq_lib.sha256_interrupt_seq import sha256_interrupt_seq
        seq = sha256_interrupt_seq("irq_test")
        await seq.start(self.env.bus_agent.sequencer)
        self.drop_objection()


@pyuvm.test()
class CoverageClosureTest(sha256_base_test):
    """Coverage closure — systematically hits all coverage bins."""

    async def run_phase(self):
        self.raise_objection()
        from seq_lib.sha256_coverage_closure_seq import sha256_coverage_closure_seq
        seq = sha256_coverage_closure_seq("cov_closure")
        await seq.start(self.env.bus_agent.sequencer)
        self.drop_objection()

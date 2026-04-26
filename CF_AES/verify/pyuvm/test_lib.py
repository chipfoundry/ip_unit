"""Test library for CF_AES verification — 7 tests covering AES-128/256 encrypt/decrypt."""

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

from ip_agent.aes_driver import aes_driver
from ip_agent.aes_monitor import aes_monitor
from ip_coverage.aes_coverage import aes_coverage
from ip_scoreboard import aes_scoreboard


class aes_env(top_env):
    """AES-specific top environment."""

    def build_phase(self):
        from cf_verify.bus_env.bus_agent import bus_agent
        from cf_verify.ip_env.ip_logger import ip_logger
        from cf_verify.base.ref_model import ref_model

        self.bus_agent = bus_agent("bus_agent", self)
        self.ip_agent = aes_ip_agent("ip_agent", self)
        self.ref_model = ref_model("ref_model", self)
        self.scoreboard = aes_scoreboard("scoreboard", self)
        self.ip_coverage = aes_coverage("ip_coverage", self)
        self.ip_logger = ip_logger("ip_logger", self)

    def connect_phase(self):
        super().connect_phase()
        self.bus_agent.monitor.ap.connect(self.ip_coverage.analysis_export)


class aes_ip_agent(ip_agent):
    driver_cls = aes_driver
    monitor_cls = aes_monitor


class aes_base_test(base_test):
    """Base test for CF_AES — sets up ConfigDB and the AES environment."""

    def build_phase(self):
        dut = cocotb.top
        bus_type = os.environ.get("BUS_TYPE", "APB")
        yaml_file = os.environ.get(
            "YAML_FILE",
            str(Path(__file__).resolve().parent.parent.parent / "CF_AES.yaml"),
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

        self.env = aes_env("env", self)
        super().build_phase()


@pyuvm.test()
class WriteReadRegsTest(aes_base_test):
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
class Encrypt128Test(aes_base_test):
    """AES-128 encryption with NIST test vector."""

    async def run_phase(self):
        self.raise_objection()
        from seq_lib.aes_encrypt_128_seq import aes_encrypt_128_seq
        seq = aes_encrypt_128_seq("enc128")
        await seq.start(self.env.bus_agent.sequencer)
        self.drop_objection()


@pyuvm.test()
class Decrypt128Test(aes_base_test):
    """AES-128 decryption with NIST test vector."""

    async def run_phase(self):
        self.raise_objection()
        from seq_lib.aes_decrypt_128_seq import aes_decrypt_128_seq
        seq = aes_decrypt_128_seq("dec128")
        await seq.start(self.env.bus_agent.sequencer)
        self.drop_objection()


@pyuvm.test()
class Encrypt256Test(aes_base_test):
    """AES-256 encryption with NIST test vector."""

    async def run_phase(self):
        self.raise_objection()
        from seq_lib.aes_encrypt_256_seq import aes_encrypt_256_seq
        seq = aes_encrypt_256_seq("enc256")
        await seq.start(self.env.bus_agent.sequencer)
        self.drop_objection()


@pyuvm.test()
class Decrypt256Test(aes_base_test):
    """AES-256 decryption with NIST test vector."""

    async def run_phase(self):
        self.raise_objection()
        from seq_lib.aes_decrypt_256_seq import aes_decrypt_256_seq
        seq = aes_decrypt_256_seq("dec256")
        await seq.start(self.env.bus_agent.sequencer)
        self.drop_objection()


@pyuvm.test()
class InterruptTest(aes_base_test):
    """Interrupt — verifies valid and ready interrupt sources."""

    async def run_phase(self):
        self.raise_objection()
        from seq_lib.aes_interrupt_seq import aes_interrupt_seq
        seq = aes_interrupt_seq("irq_test")
        await seq.start(self.env.bus_agent.sequencer)
        self.drop_objection()


@pyuvm.test()
class CoverageClosureTest(aes_base_test):
    """Coverage closure — systematically hits all coverage bins."""

    async def run_phase(self):
        self.raise_objection()
        from seq_lib.aes_coverage_closure_seq import aes_coverage_closure_seq
        seq = aes_coverage_closure_seq("cov_closure")
        await seq.start(self.env.bus_agent.sequencer)
        self.drop_objection()

"""SHA256 IP monitor — watches digest_valid and captures sha256_core outputs."""

import cocotb
from cocotb.triggers import RisingEdge, FallingEdge, Timer
from pyuvm import uvm_monitor, uvm_analysis_port, ConfigDB

from ip_item.sha256_item import sha256_item


class sha256_monitor(uvm_monitor):
    def build_phase(self):
        super().build_phase()
        self.ap = uvm_analysis_port("ap", self)
        self.dut = ConfigDB().get(self, "", "DUT")

    async def run_phase(self):
        cocotb.start_soon(self._watch_digest())

    async def _watch_digest(self):
        while True:
            await RisingEdge(self.dut.sha_digest_valid)
            await Timer(1, "ns")

            try:
                digest_val = int(self.dut.sha_digest.value)
            except ValueError:
                digest_val = 0

            try:
                ready_val = int(self.dut.sha_ready.value)
            except ValueError:
                ready_val = 0

            tr = sha256_item("sha256_digest_tr")
            tr.digest = digest_val
            tr.valid = 1
            tr.ready = ready_val
            self.logger.info(
                f"SHA256 digest captured: 0x{digest_val:064x} "
                f"ready={ready_val}"
            )
            self.ap.write(tr)

            await FallingEdge(self.dut.sha_digest_valid)

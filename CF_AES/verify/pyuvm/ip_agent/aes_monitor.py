"""AES IP monitor — watches result_valid and captures aes_core outputs."""

import cocotb
from cocotb.triggers import RisingEdge, FallingEdge, Timer
from pyuvm import uvm_monitor, uvm_analysis_port, ConfigDB

from ip_item.aes_item import aes_item


class aes_monitor(uvm_monitor):
    def build_phase(self):
        super().build_phase()
        self.ap = uvm_analysis_port("ap", self)
        self.dut = ConfigDB().get(self, "", "DUT")

    async def run_phase(self):
        cocotb.start_soon(self._watch_result())

    async def _watch_result(self):
        """Detect rising edge of result_valid and capture the result."""
        while True:
            await RisingEdge(self.dut.aes_result_valid)
            await Timer(1, "ns")

            try:
                result_val = int(self.dut.aes_result.value)
            except ValueError:
                result_val = 0

            try:
                ready_val = int(self.dut.aes_ready.value)
            except ValueError:
                ready_val = 0

            tr = aes_item("aes_result_tr")
            tr.result = result_val
            tr.valid = 1
            tr.ready = ready_val
            self.logger.info(
                f"AES result captured: 0x{result_val:032x} "
                f"ready={ready_val}"
            )
            self.ap.write(tr)

            await FallingEdge(self.dut.aes_result_valid)

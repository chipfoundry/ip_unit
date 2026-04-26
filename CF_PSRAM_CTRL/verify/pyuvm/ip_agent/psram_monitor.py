"""PSRAM IP monitor — observes the external SPI/QSPI/QPI interface signals.

Monitors sck, ce_n, dout, and din to decode PSRAM transactions. Currently
a structural placeholder; full protocol decoding requires a PSRAM model.
"""

import cocotb
from cocotb.triggers import RisingEdge, FallingEdge
from pyuvm import uvm_monitor, uvm_analysis_port, ConfigDB

from ip_item.psram_item import psram_item


class psram_ip_monitor(uvm_monitor):
    def build_phase(self):
        super().build_phase()
        self.ap = uvm_analysis_port("ap", self)
        self.dut = ConfigDB().get(self, "", "DUT")

    async def run_phase(self):
        await self._monitor()

    async def _monitor(self):
        """Watch for SPI transactions by observing ce_n falling edges."""
        while True:
            try:
                await FallingEdge(self.dut.ce_n)
            except Exception:
                await RisingEdge(self.dut.CLK)
                continue

            tr = psram_item("spi_tr")
            tr.data = 0
            self.ap.write(tr)

            try:
                await RisingEdge(self.dut.ce_n)
            except Exception:
                await RisingEdge(self.dut.CLK)

"""QSPI IP monitor — observes QSPI flash interface signals.

Monitors the SPI bus (sck, ce_n, dout, din) to decode flash read transactions.
This provides visibility into cache miss behavior at the flash interface level.
"""

import cocotb
from cocotb.triggers import RisingEdge, FallingEdge, ClockCycles
from pyuvm import uvm_monitor, uvm_analysis_port, ConfigDB

from ip_item.qspi_item import qspi_item


class qspi_monitor(uvm_monitor):
    def build_phase(self):
        super().build_phase()
        self.ap = uvm_analysis_port("ap", self)
        self.dut = ConfigDB().get(self, "", "DUT")
        self.flash_access_count = 0

    async def run_phase(self):
        cocotb.start_soon(self._watch_flash_accesses())

    async def _watch_flash_accesses(self):
        """Count flash access transactions by monitoring ce_n assertions."""
        while True:
            await FallingEdge(self.dut.ce_n)
            self.flash_access_count += 1
            tr = qspi_item("flash_access")
            tr.cache_hit = False
            self.ap.write(tr)
            await RisingEdge(self.dut.ce_n)

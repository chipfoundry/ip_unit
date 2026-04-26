"""WDT IP monitor — watches the IRQ output for timeout events."""

import cocotb
from cocotb.triggers import RisingEdge, ClockCycles
from pyuvm import uvm_monitor, uvm_analysis_port, ConfigDB

from ip_item.wdt_item import wdt_item


class wdt_monitor(uvm_monitor):
    def build_phase(self):
        super().build_phase()
        self.ap = uvm_analysis_port("ap", self)
        self.dut = ConfigDB().get(self, "", "DUT")
        self.regs = ConfigDB().get(None, "", "bus_regs")
        self.timeout_event = cocotb.triggers.Event()

    async def run_phase(self):
        cocotb.start_soon(self._watch_irq())

    async def _watch_irq(self):
        """Monitor IRQ line for timeout events."""
        while True:
            try:
                await RisingEdge(self.dut.irq)
            except Exception:
                await ClockCycles(self.dut.CLK, 1)
                continue

            tr = wdt_item("timeout_mon")
            tr.timeout = True
            tr.enabled = True
            self.ap.write(tr)
            self.timeout_event.set()

            try:
                while int(self.dut.irq.value) == 1:
                    await ClockCycles(self.dut.CLK, 1)
            except Exception:
                await ClockCycles(self.dut.CLK, 1)

"""USB CDC IP monitor — observes USB output signals (dp_tx_o, dn_tx_o, tx_en_o)."""

import cocotb
from cocotb.triggers import RisingEdge, FallingEdge, ClockCycles
from cocotb.utils import get_sim_time
from pyuvm import uvm_monitor, uvm_analysis_port, ConfigDB

from ip_item.usb_item import usb_item


class usb_monitor(uvm_monitor):
    def build_phase(self):
        super().build_phase()
        self.ap = uvm_analysis_port("ap", self)
        self.dut = ConfigDB().get(self, "", "DUT")

    async def run_phase(self):
        cocotb.start_soon(self._watch_tx_enable())

    async def _watch_tx_enable(self):
        """Monitor tx_en_o transitions to capture TX activity."""
        while True:
            try:
                await RisingEdge(self.dut.tx_en_o)
            except Exception:
                await ClockCycles(self.dut.CLK, 100)
                continue
            tr = usb_item("tx_mon")
            tr.direction = usb_item.TX
            try:
                tr.dp = int(self.dut.dp_tx_o.value)
                tr.dn = int(self.dut.dn_tx_o.value)
            except Exception:
                tr.dp = 0
                tr.dn = 0
            self.ap.write(tr)
            try:
                await FallingEdge(self.dut.tx_en_o)
            except Exception:
                await ClockCycles(self.dut.CLK, 100)

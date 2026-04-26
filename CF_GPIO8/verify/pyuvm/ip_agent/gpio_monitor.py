"""GPIO IP monitor — watches io_out and io_oe for changes."""

import cocotb
from cocotb.triggers import RisingEdge, ClockCycles, Edge
from pyuvm import uvm_monitor, uvm_analysis_port, ConfigDB

from ip_item.gpio_item import gpio_item


class gpio_monitor(uvm_monitor):
    def build_phase(self):
        super().build_phase()
        self.ap = uvm_analysis_port("ap", self)
        self.dut = ConfigDB().get(self, "", "DUT")

    async def run_phase(self):
        cocotb.start_soon(self._sample_outputs())

    async def _sample_outputs(self):
        prev_out = 0
        prev_oe = 0
        while True:
            await RisingEdge(self.dut.CLK)
            try:
                cur_out = int(self.dut.io_out.value)
            except ValueError:
                cur_out = 0
            try:
                cur_oe = int(self.dut.io_oe.value)
            except ValueError:
                cur_oe = 0

            if cur_out != prev_out or cur_oe != prev_oe:
                tr = gpio_item("out_mon")
                tr.data = cur_out
                tr.direction = cur_oe
                tr.is_input = False
                self.ap.write(tr)
                prev_out = cur_out
                prev_oe = cur_oe

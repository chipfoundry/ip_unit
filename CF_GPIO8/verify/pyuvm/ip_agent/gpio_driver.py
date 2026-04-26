"""GPIO IP driver — drives io_in pins from the external interface side."""

import cocotb
from cocotb.triggers import ClockCycles, Timer
from pyuvm import uvm_driver, ConfigDB

from ip_item.gpio_item import gpio_item


class gpio_driver(uvm_driver):
    def build_phase(self):
        super().build_phase()
        self.dut = ConfigDB().get(self, "", "DUT")

    async def run_phase(self):
        while True:
            item = await self.seq_item_port.get_next_item()
            if isinstance(item, gpio_item) and item.is_input:
                self.dut.io_in.value = item.data & 0xFF
                await ClockCycles(self.dut.CLK, 3)
            self.logger.info(f"GPIO driver: {item.convert2string()}")
            self.seq_item_port.item_done()

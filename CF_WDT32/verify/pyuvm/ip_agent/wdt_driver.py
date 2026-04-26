"""WDT IP driver — minimal driver since the WDT has no external protocol inputs.

The WDT is controlled entirely via bus register writes (load, control).
This driver handles any IP-side sequence items but does not need to drive
external signals.
"""

from pyuvm import uvm_driver, ConfigDB


class wdt_driver(uvm_driver):
    def build_phase(self):
        super().build_phase()
        self.dut = ConfigDB().get(self, "", "DUT")
        self.regs = ConfigDB().get(None, "", "bus_regs")

    async def run_phase(self):
        while True:
            item = await self.seq_item_port.get_next_item()
            self.logger.info(f"WDT driver got item: {item.convert2string()}")
            self.seq_item_port.item_done()

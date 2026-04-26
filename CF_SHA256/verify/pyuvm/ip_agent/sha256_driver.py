"""SHA256 IP driver — minimal since SHA256 is entirely register-controlled."""

from pyuvm import uvm_driver, ConfigDB


class sha256_driver(uvm_driver):
    def build_phase(self):
        super().build_phase()
        self.dut = ConfigDB().get(self, "", "DUT")

    async def run_phase(self):
        while True:
            item = await self.seq_item_port.get_next_item()
            self.logger.info(f"SHA256 driver received: {item.convert2string()}")
            self.seq_item_port.item_done()

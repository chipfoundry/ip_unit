"""AES IP driver — minimal since AES is entirely register-controlled."""

from pyuvm import uvm_driver, ConfigDB


class aes_driver(uvm_driver):
    """AES has no external data pins to drive (no TX/RX lines).

    All stimulus is delivered through the bus agent by writing registers.
    This driver exists to satisfy the ip_agent component hierarchy and
    can be extended if direct-port-drive testing is needed in the future.
    """

    def build_phase(self):
        super().build_phase()
        self.dut = ConfigDB().get(self, "", "DUT")

    async def run_phase(self):
        while True:
            item = await self.seq_item_port.get_next_item()
            self.logger.info(f"AES driver received: {item.convert2string()}")
            self.seq_item_port.item_done()

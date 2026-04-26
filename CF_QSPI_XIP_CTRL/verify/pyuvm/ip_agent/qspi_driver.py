"""QSPI IP driver — configures the flash VIP memory contents.

Unlike register-based IPs, the QSPI controller has no writable registers.
The driver's role is limited to loading initial memory contents into the
SST26WF080B flash VIP model before simulation begins.
"""

import cocotb
from cocotb.triggers import RisingEdge, Timer
from pyuvm import uvm_driver, ConfigDB


class qspi_driver(uvm_driver):
    def build_phase(self):
        super().build_phase()
        self.dut = ConfigDB().get(self, "", "DUT")

    async def run_phase(self):
        while True:
            item = await self.seq_item_port.get_next_item()
            self.logger.info(f"QSPI driver: item received (no-op, read-only IP)")
            self.seq_item_port.item_done()

    def load_flash_memory(self, memory_bytes):
        """Load memory contents into the SST26WF080B VIP.
        Must be called after elaboration when VIP hierarchy is accessible."""
        try:
            vip_mem = self.dut.vip.I0.memory
            for i, byte_val in enumerate(memory_bytes):
                vip_mem[i].value = byte_val
            self.logger.info(
                f"Loaded {len(memory_bytes)} bytes into flash VIP memory"
            )
        except AttributeError:
            self.logger.warning(
                "Cannot access vip.I0.memory — flash VIP memory not loaded"
            )

"""USB CDC IP driver — drives dp_rx_i and dn_rx_i signals for basic USB stimulation.

Without a full USB host model, this driver provides basic signaling:
idle (J state), SE0 for reset, and simple bit-level toggling. Protocol-level
USB transactions (token, data, handshake packets) are beyond scope here.
"""

import cocotb
from cocotb.triggers import ClockCycles, FallingEdge, First
from pyuvm import uvm_driver, ConfigDB

from ip_item.usb_item import usb_item


class usb_driver(uvm_driver):
    def build_phase(self):
        super().build_phase()
        self.dut = ConfigDB().get(self, "", "DUT")

    async def run_phase(self):
        self.dut.dp_rx_i.value = 1
        self.dut.dn_rx_i.value = 0
        while True:
            item = await self.seq_item_port.get_next_item()
            if item.direction == usb_item.RX:
                self.logger.info(f"Driving USB RX: {item.convert2string()}")
                drive_thread = cocotb.start_soon(self._drive_usb_rx(item))
                reset_thread = cocotb.start_soon(self._wait_reset())
                await First(drive_thread, reset_thread)
                self.dut.dp_rx_i.value = 1
                self.dut.dn_rx_i.value = 0
                reset_thread.kill()
                drive_thread.kill()
            self.seq_item_port.item_done()

    async def _wait_reset(self):
        await FallingEdge(self.dut.RESETn)

    async def _drive_usb_rx(self, tr):
        """Drive D+/D- with item values for a few clock cycles."""
        self.dut.dp_rx_i.value = tr.dp
        self.dut.dn_rx_i.value = tr.dn
        await ClockCycles(self.dut.CLK, 10)
        self.dut.dp_rx_i.value = 1
        self.dut.dn_rx_i.value = 0

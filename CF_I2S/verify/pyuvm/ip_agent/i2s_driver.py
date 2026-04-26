"""I2S IP driver — drives SDI line to simulate an I2S transmitter (microphone)."""

import cocotb
from cocotb.triggers import FallingEdge, RisingEdge, First
from pyuvm import uvm_driver, ConfigDB

from ip_item.i2s_item import i2s_item


class i2s_driver(uvm_driver):
    def build_phase(self):
        super().build_phase()
        self.dut = ConfigDB().get(self, "", "DUT")
        self.regs = ConfigDB().get(None, "", "bus_regs")

    async def run_phase(self):
        self.dut.SDI.value = 0
        while True:
            item = await self.seq_item_port.get_next_item()
            self.logger.info(f"Driving SDI: {item.convert2string()}")
            send_thread = cocotb.start_soon(self._send_item(item))
            reset_thread = cocotb.start_soon(self._wait_reset())
            await First(send_thread, reset_thread)
            self.dut.SDI.value = 0
            reset_thread.kill()
            send_thread.kill()
            self.seq_item_port.item_done()

    async def _wait_reset(self):
        await FallingEdge(self.dut.RESETn)

    async def _send_item(self, tr):
        """Drive sample data on SDI, MSB-first, on falling edge of SCK.

        Standard I2S timing: data transitions on falling SCK edge,
        sampled by receiver on rising SCK edge.
        WS=0 => left channel, WS=1 => right channel.
        Data starts one SCK cycle after WS transition.
        """
        cfg = self.regs.read_reg_value("CFG")
        left_justified = (cfg >> 3) & 1
        sample_size = ((cfg >> 4) & 0x3F) or 32

        target_ws = 1 if tr.channel == i2s_item.RIGHT else 0

        # Wait for the correct WS phase
        while True:
            await RisingEdge(self.dut.sck)
            try:
                ws_val = int(self.dut.ws.value)
            except Exception:
                continue
            if ws_val == target_ws:
                break

        if not left_justified:
            # Standard I2S: one SCK delay after WS transition
            await FallingEdge(self.dut.sck)

        # Drive data bits MSB-first on falling edges of SCK
        for i in range(sample_size):
            await FallingEdge(self.dut.sck)
            bit = (tr.sample_data >> (sample_size - 1 - i)) & 1
            self.dut.SDI.value = bit

        # Clear SDI after sending
        await FallingEdge(self.dut.sck)
        self.dut.SDI.value = 0

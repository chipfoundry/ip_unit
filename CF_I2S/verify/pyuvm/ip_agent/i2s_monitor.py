"""I2S IP monitor — observes ws, sck, sdi signals and captures received audio samples."""

import cocotb
from cocotb.triggers import RisingEdge, FallingEdge
from pyuvm import uvm_monitor, uvm_analysis_port, ConfigDB

from ip_item.i2s_item import i2s_item


class i2s_monitor(uvm_monitor):
    def build_phase(self):
        super().build_phase()
        self.ap = uvm_analysis_port("ap", self)
        self.dut = ConfigDB().get(self, "", "DUT")
        self.regs = ConfigDB().get(None, "", "bus_regs")

    async def run_phase(self):
        cocotb.start_soon(self._capture_samples())

    async def _capture_samples(self):
        """Continuously monitor the I2S bus and capture samples."""
        while True:
            try:
                await RisingEdge(self.dut.sck)
            except Exception:
                return

            cfg = self.regs.read_reg_value("CFG")
            sample_size = ((cfg >> 4) & 0x3F) or 32
            left_justified = (cfg >> 3) & 1

            # Detect WS transitions to start capturing
            try:
                prev_ws = int(self.dut.ws.value)
            except Exception:
                continue

            await RisingEdge(self.dut.sck)
            try:
                cur_ws = int(self.dut.ws.value)
            except Exception:
                continue

            if prev_ws == cur_ws:
                continue

            channel = i2s_item.RIGHT if cur_ws == 1 else i2s_item.LEFT

            if not left_justified:
                # Standard I2S: skip one SCK cycle after WS transition
                await RisingEdge(self.dut.sck)

            # Capture data bits on rising edges of SCK (MSB-first)
            data = 0
            for i in range(sample_size):
                await RisingEdge(self.dut.sck)
                try:
                    bit = int(self.dut.SDI.value)
                except Exception:
                    bit = 0
                data = (data << 1) | bit

            tr = i2s_item("mon_tr")
            tr.sample_data = data
            tr.channel = channel
            tr.sample_size = sample_size
            self.ap.write(tr)
            self.logger.debug(f"Captured: {tr.convert2string()}")

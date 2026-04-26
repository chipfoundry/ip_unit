"""PSRAM IP driver — stub driver for the external QSPI interface.

Without a full PSRAM memory model, this driver provides loopback-style
responses on the din lines. For full memory-access testing, replace with
a driver that interfaces with a Verilog PSRAM model (e.g. M23LC1024).
"""

from pyuvm import ConfigDB

from cf_verify.ip_env.ip_driver import ip_driver


class psram_ip_driver(ip_driver):
    def build_phase(self):
        super().build_phase()
        self.dut = ConfigDB().get(self, "", "DUT")

    async def _drive(self, item):
        pass

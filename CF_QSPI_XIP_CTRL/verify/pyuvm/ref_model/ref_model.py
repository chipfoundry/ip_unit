"""QSPI XIP reference model — models the flash memory content for read verification.

Since the IP has no registers, the reference model simply stores flash memory
contents and returns the expected 32-bit word for any given address.
"""

import cocotb
from pyuvm import ConfigDB

from cf_verify.base.ref_model import ref_model
from cf_verify.bus_env.bus_item import bus_item


class QSPI_VIP(ref_model):
    def build_phase(self):
        super().build_phase()
        self.flash_memory = None
        self.flash_size = 0
        try:
            self.flash_memory = ConfigDB().get(None, "", "flash_memory")
            self.flash_size = ConfigDB().get(None, "", "flash_size")
        except Exception:
            self.logger.warning(
                "No flash_memory in ConfigDB — ref model will return 0 for reads"
            )

    def write_bus(self, tr):
        if tr.kind == bus_item.RESET:
            self.bus_out.write(tr)
            return
        if tr.kind == bus_item.READ:
            data = self._get_memory_value(tr.addr)
            td = tr.do_clone()
            td.data = data
            self.bus_out.write(td)
        elif tr.kind == bus_item.WRITE:
            self.bus_out.write(tr)

    def write_ip(self, tr):
        pass

    def _get_memory_value(self, address):
        if self.flash_memory is None:
            return 0
        if address + 3 >= self.flash_size:
            return 0
        return (
            self.flash_memory[address]
            | (self.flash_memory[address + 1] << 8)
            | (self.flash_memory[address + 2] << 16)
            | (self.flash_memory[address + 3] << 24)
        )

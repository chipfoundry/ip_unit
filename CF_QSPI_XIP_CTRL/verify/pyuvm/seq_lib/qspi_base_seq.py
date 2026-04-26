"""Base sequence for QSPI XIP controller — provides AHB read helpers."""

import random

from pyuvm import uvm_sequence, uvm_root, ConfigDB
from cf_verify.bus_env.bus_item import bus_item
from cf_verify.bus_env.bus_seq_lib import reset_seq


class qspi_base_seq(uvm_sequence):
    def __init__(self, name="qspi_base_seq", memory_size=0x100000):
        super().__init__(name)
        self.memory_size = memory_size
        self._flash_memory = None

    def _get_flash(self):
        if self._flash_memory is None:
            try:
                self._flash_memory = ConfigDB().get(None, "", "flash_memory")
            except Exception:
                pass
        return self._flash_memory

    def _expected_word(self, address):
        """Return expected little-endian 32-bit word from flash at address."""
        fm = self._get_flash()
        if fm is None or address + 3 >= len(fm):
            return None
        return (
            fm[address] | (fm[address + 1] << 8)
            | (fm[address + 2] << 16) | (fm[address + 3] << 24)
        )

    async def body(self):
        await reset_seq("rst").start(self.sequencer)

    async def ahb_read(self, address):
        """Issue an AHB read transaction at the given address."""
        req = bus_item("ahb_read")
        req.addr = address & 0xFFFFFFFC
        req.kind = bus_item.READ
        req.data = 0
        await self.start_item(req)
        await self.finish_item(req)
        return req

    async def ahb_read_check(self, address):
        """Issue an AHB read and verify against flash contents."""
        req = await self.ahb_read(address)
        expected = self._expected_word(address & 0xFFFFFFFC)
        if expected is not None and req.data is not None:
            actual = req.data & 0xFFFFFFFF
            assert actual == expected, (
                f"QSPI flash read mismatch at 0x{address:06x}: "
                f"expected 0x{expected:08x}, got 0x{actual:08x}"
            )
        return req

    async def read_bulk(self, start_address, count=8):
        """Issue a sequence of consecutive AHB reads."""
        results = []
        addr = start_address & 0xFFFFFFFC
        for _ in range(count):
            if addr >= self.memory_size:
                break
            req = await self.ahb_read_check(addr)
            results.append(req)
            addr += 4
        return results

    async def read_random(self, count=16):
        """Issue random AHB reads across the address space."""
        results = []
        for _ in range(count):
            addr = random.randrange(0, self.memory_size, 4)
            req = await self.ahb_read_check(addr)
            results.append(req)
        return results

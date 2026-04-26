"""Cache miss/hit sequences — exercise cache behavior across all address ranges.

Reads the same address twice (should hit on second access), then reads
addresses that map to different cache lines to force evictions.
"""

import random
from seq_lib.qspi_base_seq import qspi_base_seq
from cf_verify.bus_env.bus_seq_lib import reset_seq


class qspi_cache_miss_seq(qspi_base_seq):
    """Force cache misses by reading addresses that map to distinct lines."""

    def __init__(self, name="qspi_cache_miss_seq", memory_size=0x100000):
        super().__init__(name, memory_size)

    async def body(self):
        await reset_seq("rst").start(self.sequencer)

        line_size = 32
        num_lines = 16
        stride = line_size

        for i in range(num_lines + 4):
            addr = i * stride
            await self.ahb_read(addr)

        # Also miss in high_1M region
        if self.memory_size > 0x10000:
            base = 0x80000
            for i in range(8):
                await self.ahb_read(base + i * stride)


class qspi_sequential_read_seq(qspi_base_seq):
    """Read sequential addresses to test cache line fill and reuse."""

    def __init__(self, name="qspi_sequential_read_seq", memory_size=0x100000):
        super().__init__(name, memory_size)

    async def body(self):
        await reset_seq("rst").start(self.sequencer)

        # mid_64K region: first pass (miss), second pass (hit)
        base = 0x1000
        for offset in range(0, 128, 4):
            await self.ahb_read(base + offset)
        for offset in range(0, 128, 4):
            await self.ahb_read(base + offset)

        # high_1M region: first pass (miss), second pass (hit)
        if self.memory_size > 0x10000:
            base = 0x50000
            for offset in range(0, 128, 4):
                await self.ahb_read(base + offset)
            for offset in range(0, 128, 4):
                await self.ahb_read(base + offset)

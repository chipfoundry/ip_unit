"""Flash read sequence — reads addresses from all flash regions via AHB."""

import random
from seq_lib.qspi_base_seq import qspi_base_seq
from cf_verify.bus_env.bus_seq_lib import reset_seq


class qspi_read_seq(qspi_base_seq):
    def __init__(self, name="qspi_read_seq", memory_size=0x100000):
        super().__init__(name, memory_size)

    async def body(self):
        await reset_seq("rst").start(self.sequencer)

        # low_4K region
        await self.ahb_read(0x000000)
        await self.ahb_read(0x000004)
        await self.ahb_read(0x000008)

        for _ in range(3):
            address = random.randrange(0, min(self.memory_size, 0x1000), 4)
            await self.read_bulk(address, count=random.randint(4, 8))

        # mid_64K region
        for _ in range(3):
            address = random.randrange(0x1000, min(self.memory_size, 0x10000), 4)
            await self.read_bulk(address, count=random.randint(4, 8))

        # high_1M region
        if self.memory_size > 0x10000:
            for _ in range(3):
                address = random.randrange(0x10000, self.memory_size, 4)
                await self.read_bulk(address, count=random.randint(4, 8))

        # Re-read earlier addresses to generate cache hits
        await self.ahb_read(0x000000)
        await self.ahb_read(0x000004)

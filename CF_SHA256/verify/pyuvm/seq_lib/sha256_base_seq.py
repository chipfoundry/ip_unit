"""Base SHA256 sequence with common helper methods."""

from pyuvm import uvm_sequence, ConfigDB
from cocotb.triggers import ClockCycles

from cf_verify.bus_env.bus_seq_lib import write_reg_seq, read_reg_seq, reset_seq


class sha256_base_seq(uvm_sequence):
    async def _init(self):
        await reset_seq("rst").start(self.sequencer)

        self.regs = ConfigDB().get(None, "", "bus_regs")
        self.dut = ConfigDB().get(None, "", "DUT")
        self.addr = self.regs.reg_name_to_address

        if "GCLK" in self.addr:
            await self._w("gclk", "GCLK", 1)

    async def _w(self, name, reg, val):
        await write_reg_seq(name, self.addr[reg], val).start(self.sequencer)

    async def _r(self, name, reg):
        seq = read_reg_seq(name, self.addr[reg])
        await seq.start(self.sequencer)
        return seq.result

    async def _write_block(self, block_512):
        """Write a 512-bit block into BLOCK0-BLOCK15."""
        for i in range(16):
            val = (block_512 >> (i * 32)) & 0xFFFFFFFF
            await self._w(f"blk{i}", f"BLOCK{i}", val)

    async def _hash(self, block_512, mode=1, is_first=True):
        """Run one SHA hash round: init or next, then poll for completion."""
        await self._write_block(block_512)

        if is_first:
            ctrl = (mode << 2) | 0x01  # init=1
        else:
            ctrl = (mode << 2) | 0x02  # next=1

        await self._w("ctrl", "CTRL", ctrl)
        ctrl_base = mode << 2
        await self._w("ctrl_clr", "CTRL", ctrl_base)

        for _ in range(500):
            st = await self._r("poll_valid", "STATUS")
            if (st >> 7) & 1:
                break
            await ClockCycles(self.dut.CLK, 10)

    async def _read_digest(self):
        """Read DIGEST0-DIGEST7 via bus, return 256-bit value."""
        digest = 0
        for i in range(8):
            val = await self._r(f"dig{i}", f"DIGEST{i}")
            digest |= ((val or 0) & 0xFFFFFFFF) << (i * 32)
        return digest

    async def _read_digest_from_core(self):
        """Read digest directly from sha256_core through hierarchy."""
        try:
            return int(self.dut.sha_digest.value)
        except (ValueError, AttributeError):
            return 0

"""Coverage closure sequence — systematically hits all SHA256 coverage bins."""

from seq_lib.sha256_base_seq import sha256_base_seq

ABC_BLOCK = 0x61626380000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000018

NONZERO_BLOCK = 0xdeadbeefcafebabe123456789abcdef00fedcba987654321aabbccddeeff001122334455667788990011223344556677deadbeefcafebabe0011223344556677


class sha256_coverage_closure_seq(sha256_base_seq):
    async def body(self):
        await self._init()

        await self._ctrl_bins()
        await self._mode_coverage()
        await self._block_bins()
        await self._interrupt_bins()
        await self._register_read_bins()

    async def _ctrl_bins(self):
        """Hit all CTRL field combinations."""
        ctrl_vals = [
            0x00,
            0x01,  # init only
            0x02,  # next only
            0x04,  # mode only
            0x03,  # init + next
            0x05,  # init + mode
            0x06,  # next + mode
            0x07,  # all bits
        ]
        for ctrl in ctrl_vals:
            await self._w("ctrl_cov", "CTRL", ctrl)

    async def _mode_coverage(self):
        """Cover both SHA-224 (mode=0) and SHA-256 (mode=1) with actual hashing."""
        from cocotb.triggers import ClockCycles

        await self._r("status_idle", "STATUS")
        await self._r("ris_idle", "RIS")

        await self._write_block(ABC_BLOCK)
        await self._w("ctrl_init256", "CTRL", (1 << 2) | 0x01)
        await self._w("ctrl_clr256", "CTRL", (1 << 2))
        await self._r("status_busy", "STATUS")
        await ClockCycles(self.dut.CLK, 5)
        await self._r("status_busy2", "STATUS")

        for _ in range(500):
            st = await self._r("poll_val256", "STATUS")
            if (st >> 7) & 1:
                break
            await ClockCycles(self.dut.CLK, 10)

        await self._read_digest()
        await self._r("status_sha256", "STATUS")
        await self._r("ris_sha256", "RIS")

        await self._w("ic_clr", "IC", 0x3)

        await self._hash(ABC_BLOCK, mode=0, is_first=True)
        await self._read_digest()
        await self._r("status_sha224", "STATUS")
        await self._r("ris_sha224", "RIS")

    async def _block_bins(self):
        """Write zero and non-zero values to all BLOCK registers for bin coverage."""
        for i in range(16):
            await self._w(f"blk_zero_{i}", f"BLOCK{i}", 0)

        await self._write_block(NONZERO_BLOCK)

    async def _interrupt_bins(self):
        """Exercise interrupt mask, status, and clear registers."""
        await self._w("im_all", "IM", 0x3)

        await self._hash(ABC_BLOCK, mode=1, is_first=True)
        await self._r("ris_cov", "RIS")
        await self._r("mis_cov", "MIS")

        await self._w("ic_cov", "IC", 0x3)
        await self._r("ris_clr", "RIS")

        await self._w("im_0", "IM", 0x1)
        await self._r("im_rd0", "IM")
        await self._w("im_1", "IM", 0x2)
        await self._r("im_rd1", "IM")
        await self._w("im_all2", "IM", 0x3)

    async def _register_read_bins(self):
        """Read all register addresses to cover the bus read mux."""
        await self._r("st", "STATUS")
        for i in range(16):
            await self._r(f"blk_rd{i}", f"BLOCK{i}")
        for i in range(8):
            await self._r(f"dig_rd{i}", f"DIGEST{i}")
        await self._r("im_rd", "IM")
        await self._r("mis_rd", "MIS")
        await self._r("ris_rd", "RIS")

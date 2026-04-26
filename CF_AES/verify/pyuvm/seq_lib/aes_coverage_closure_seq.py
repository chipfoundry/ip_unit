"""Coverage closure sequence — systematically hits all AES coverage bins."""

from pyuvm import uvm_sequence, ConfigDB
from cocotb.triggers import ClockCycles

from cf_verify.bus_env.bus_seq_lib import write_reg_seq, read_reg_seq, reset_seq

NIST_KEY_128 = 0x2b7e151628aed2a6abf7158809cf4f3c
NIST_KEY_256 = 0x603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4
NIST_PLAIN   = 0x6bc1bee22e409f96e93d7e117393172a


class aes_coverage_closure_seq(uvm_sequence):
    async def body(self):
        await reset_seq("rst").start(self.sequencer)

        regs = ConfigDB().get(None, "", "bus_regs")
        self.dut = ConfigDB().get(None, "", "DUT")
        self.addr = regs.reg_name_to_address

        if "GCLK" in self.addr:
            await self._w("gclk", "GCLK", 1)

        await self._ctrl_bins()
        await self._key_len_enc_dec_cross()
        await self._interrupt_bins()
        await self._register_read_bins()

    async def _w(self, name, reg, val):
        await write_reg_seq(name, self.addr[reg], val).start(self.sequencer)

    async def _r(self, name, reg):
        seq = read_reg_seq(name, self.addr[reg])
        await seq.start(self.sequencer)
        return seq.result

    async def _write_key(self, key, is_256=False):
        n = 8 if is_256 else 4
        for i in range(n):
            val = (key >> (i * 32)) & 0xFFFFFFFF
            await self._w(f"key{i}", f"KEY{i}", val)
        if not is_256:
            for i in range(4, 8):
                await self._w(f"key{i}", f"KEY{i}", 0)

    async def _write_block(self, block):
        for i in range(4):
            val = (block >> (i * 32)) & 0xFFFFFFFF
            await self._w(f"blk{i}", f"BLOCK{i}", val)

    async def _run_aes_op(self, encdec, keylen):
        """Run a complete AES init+next cycle."""
        ctrl = (encdec << 2) | (keylen << 3) | (1 << 0)
        await self._w("ctrl_init", "CTRL", ctrl)
        ctrl_base = (encdec << 2) | (keylen << 3)
        await self._w("ctrl_clr", "CTRL", ctrl_base)

        for _ in range(200):
            st = await self._r("poll_rdy", "STATUS")
            if (st >> 6) & 1:
                break
            await ClockCycles(self.dut.CLK, 10)

        ctrl = ctrl_base | (1 << 1)
        await self._w("ctrl_next", "CTRL", ctrl)
        await self._w("ctrl_clr_next", "CTRL", ctrl_base)

        for _ in range(200):
            st = await self._r("poll_val", "STATUS")
            if (st >> 7) & 1:
                break
            await ClockCycles(self.dut.CLK, 10)

        await self._r("status_final", "STATUS")
        for i in range(4):
            await self._r(f"res{i}", f"RESULT{i}")
        await self._r("ris_post_op", "RIS")

    async def _ctrl_bins(self):
        """Hit all CTRL field combinations."""
        ctrl_vals = [
            0x00,
            0x01,  # init only
            0x02,  # next only
            0x04,  # encdec only
            0x08,  # keylen only
            0x05,  # encdec + init
            0x06,  # encdec + next
            0x09,  # keylen + init
            0x0A,  # keylen + next
            0x0C,  # keylen + encdec
            0x0F,  # all bits
        ]
        for ctrl in ctrl_vals:
            await self._w("ctrl_cov", "CTRL", ctrl)

    async def _key_len_enc_dec_cross(self):
        """Cover all 4 combinations: {128,256} x {encrypt,decrypt}."""
        # AES-128 encrypt
        await self._write_key(NIST_KEY_128, is_256=False)
        await self._write_block(NIST_PLAIN)
        await self._run_aes_op(encdec=1, keylen=0)

        # AES-128 decrypt
        await self._write_key(NIST_KEY_128, is_256=False)
        await self._write_block(NIST_PLAIN)
        await self._run_aes_op(encdec=0, keylen=0)

        # AES-256 encrypt
        await self._write_key(NIST_KEY_256, is_256=True)
        await self._write_block(NIST_PLAIN)
        await self._run_aes_op(encdec=1, keylen=1)

        # AES-256 decrypt
        await self._write_key(NIST_KEY_256, is_256=True)
        await self._write_block(NIST_PLAIN)
        await self._run_aes_op(encdec=0, keylen=1)

    async def _interrupt_bins(self):
        """Exercise interrupt mask, status, and clear registers."""
        # Enable all IRQs
        await self._w("im_all", "IM", 0x3)

        # Run an operation to trigger valid+ready IRQs
        await self._write_key(NIST_KEY_128, is_256=False)
        await self._write_block(NIST_PLAIN)
        await self._run_aes_op(encdec=1, keylen=0)

        await self._r("ris_cov", "RIS")
        await self._r("mis_cov", "MIS")

        # Clear and re-check
        await self._w("ic_cov", "IC", 0x3)
        await self._r("ris_clr", "RIS")

        # Individual mask bits
        await self._w("im_0", "IM", 0x1)
        await self._r("im_rd0", "IM")
        await self._w("im_1", "IM", 0x2)
        await self._r("im_rd1", "IM")
        await self._w("im_all2", "IM", 0x3)

    async def _register_read_bins(self):
        """Read all register addresses to cover the bus read mux."""
        await self._r("st", "STATUS")
        for i in range(8):
            await self._r(f"key_rd{i}", f"KEY{i}")
        for i in range(4):
            await self._r(f"blk_rd{i}", f"BLOCK{i}")
        for i in range(4):
            await self._r(f"res_rd{i}", f"RESULT{i}")
        await self._r("im_rd", "IM")
        await self._r("mis_rd", "MIS")
        await self._r("ris_rd", "RIS")

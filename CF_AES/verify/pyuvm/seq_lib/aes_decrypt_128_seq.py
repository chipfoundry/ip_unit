"""AES-128 decryption sequence — uses NIST test vector (reverse of encrypt)."""

from pyuvm import uvm_sequence, ConfigDB
from cocotb.triggers import ClockCycles

from cf_verify.bus_env.bus_seq_lib import write_reg_seq, read_reg_seq, reset_seq

NIST_KEY_128 = 0x2b7e151628aed2a6abf7158809cf4f3c
NIST_CIPHER  = 0x3ad77bb40d7a3660a89ecaf32466ef97
NIST_PLAIN   = 0x6bc1bee22e409f96e93d7e117393172a


class aes_decrypt_128_seq(uvm_sequence):
    async def body(self):
        await reset_seq("rst").start(self.sequencer)

        regs = ConfigDB().get(None, "", "bus_regs")
        dut  = ConfigDB().get(None, "", "DUT")
        addr = regs.reg_name_to_address

        if "GCLK" in addr:
            await write_reg_seq("gclk", addr["GCLK"], 1).start(self.sequencer)

        # AES-128 key goes into KEY4-KEY7 (maps to key[255:128], where
        # aes_key_mem reads it for 128-bit mode). KEY0-KEY3 are zeroed.
        key = NIST_KEY_128
        for i in range(4):
            await write_reg_seq(f"key{i}", addr[f"KEY{i}"], 0).start(self.sequencer)
        for i in range(4):
            val = (key >> (i * 32)) & 0xFFFFFFFF
            await write_reg_seq(f"key{i+4}", addr[f"KEY{i+4}"], val).start(self.sequencer)

        # Write ciphertext as input block
        block = NIST_CIPHER
        for i in range(4):
            val = (block >> (i * 32)) & 0xFFFFFFFF
            await write_reg_seq(f"blk{i}", addr[f"BLOCK{i}"], val).start(self.sequencer)

        # CTRL: encdec=0 (decrypt), keylen=0 (128-bit), init=1
        ctrl = (0 << 2) | (0 << 3) | (1 << 0)
        await write_reg_seq("ctrl_init", addr["CTRL"], ctrl).start(self.sequencer)
        ctrl_base = (0 << 2) | (0 << 3)
        await write_reg_seq("ctrl_clr_init", addr["CTRL"], ctrl_base).start(self.sequencer)

        for _ in range(200):
            seq = read_reg_seq("poll_ready", addr["STATUS"])
            await seq.start(self.sequencer)
            if (seq.result >> 6) & 1:
                break
            await ClockCycles(dut.CLK, 10)

        ctrl = ctrl_base | (1 << 1)
        await write_reg_seq("ctrl_next", addr["CTRL"], ctrl).start(self.sequencer)
        await write_reg_seq("ctrl_clr_next", addr["CTRL"], ctrl_base).start(self.sequencer)

        for _ in range(200):
            seq = read_reg_seq("poll_valid", addr["STATUS"])
            await seq.start(self.sequencer)
            if (seq.result >> 7) & 1:
                break
            await ClockCycles(dut.CLK, 10)

        try:
            result = int(dut.aes_result.value)
        except (ValueError, AttributeError):
            result = 0

        expected = NIST_PLAIN
        assert result == expected, (
            f"AES-128 decrypt MISMATCH: "
            f"expected 0x{expected:032x}, got 0x{result:032x}"
        )

        for i in range(4):
            await read_reg_seq(f"res{i}", addr[f"RESULT{i}"]).start(self.sequencer)

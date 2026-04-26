"""AES-256 decryption sequence — uses NIST test vector (reverse of encrypt)."""

from pyuvm import uvm_sequence, ConfigDB
from cocotb.triggers import ClockCycles

from cf_verify.bus_env.bus_seq_lib import write_reg_seq, read_reg_seq, reset_seq

NIST_KEY_256 = 0x603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4
NIST_CIPHER  = 0xf3eed1bdb5d2a03c064b5a7e3db181f8
NIST_PLAIN   = 0x6bc1bee22e409f96e93d7e117393172a


class aes_decrypt_256_seq(uvm_sequence):
    async def body(self):
        await reset_seq("rst").start(self.sequencer)

        regs = ConfigDB().get(None, "", "bus_regs")
        dut  = ConfigDB().get(None, "", "DUT")
        addr = regs.reg_name_to_address

        if "GCLK" in addr:
            await write_reg_seq("gclk", addr["GCLK"], 1).start(self.sequencer)

        key = NIST_KEY_256
        for i in range(8):
            val = (key >> (i * 32)) & 0xFFFFFFFF
            await write_reg_seq(f"key{i}", addr[f"KEY{i}"], val).start(self.sequencer)

        block = NIST_CIPHER
        for i in range(4):
            val = (block >> (i * 32)) & 0xFFFFFFFF
            await write_reg_seq(f"blk{i}", addr[f"BLOCK{i}"], val).start(self.sequencer)

        # CTRL: encdec=0 (decrypt), keylen=1 (256-bit), init=1
        ctrl = (0 << 2) | (1 << 3) | (1 << 0)
        await write_reg_seq("ctrl_init", addr["CTRL"], ctrl).start(self.sequencer)
        ctrl_base = (0 << 2) | (1 << 3)
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
            f"AES-256 decrypt MISMATCH: "
            f"expected 0x{expected:032x}, got 0x{result:032x}"
        )

        for i in range(4):
            await read_reg_seq(f"res{i}", addr[f"RESULT{i}"]).start(self.sequencer)

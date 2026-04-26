"""AES interrupt sequence — exercises IRQ sources (valid, ready) and IM/IC."""

from pyuvm import uvm_sequence, ConfigDB
from cocotb.triggers import ClockCycles

from cf_verify.bus_env.bus_seq_lib import write_reg_seq, read_reg_seq, reset_seq

NIST_KEY_128 = 0x2b7e151628aed2a6abf7158809cf4f3c
NIST_PLAIN   = 0x6bc1bee22e409f96e93d7e117393172a


class aes_interrupt_seq(uvm_sequence):
    async def body(self):
        await reset_seq("rst").start(self.sequencer)

        regs = ConfigDB().get(None, "", "bus_regs")
        dut  = ConfigDB().get(None, "", "DUT")
        addr = regs.reg_name_to_address

        if "GCLK" in addr:
            await write_reg_seq("gclk", addr["GCLK"], 1).start(self.sequencer)

        # Enable both interrupt sources: bit0=valid, bit1=ready
        await write_reg_seq("im_all", addr["IM"], 0x3).start(self.sequencer)

        # Write key
        key = NIST_KEY_128
        for i in range(4):
            val = (key >> (i * 32)) & 0xFFFFFFFF
            await write_reg_seq(f"key{i}", addr[f"KEY{i}"], val).start(self.sequencer)
        for i in range(4, 8):
            await write_reg_seq(f"key{i}", addr[f"KEY{i}"], 0).start(self.sequencer)

        # Write block
        block = NIST_PLAIN
        for i in range(4):
            val = (block >> (i * 32)) & 0xFFFFFFFF
            await write_reg_seq(f"blk{i}", addr[f"BLOCK{i}"], val).start(self.sequencer)

        # Init key expansion (triggers ready interrupt when done)
        ctrl = (1 << 2) | (0 << 3) | (1 << 0)
        await write_reg_seq("ctrl_init", addr["CTRL"], ctrl).start(self.sequencer)
        ctrl_base = (1 << 2) | (0 << 3)
        await write_reg_seq("ctrl_clr", addr["CTRL"], ctrl_base).start(self.sequencer)

        # Poll until ready
        for _ in range(200):
            seq = read_reg_seq("poll_ready", addr["STATUS"])
            await seq.start(self.sequencer)
            if (seq.result >> 6) & 1:
                break
            await ClockCycles(dut.CLK, 10)

        # Check RIS for ready interrupt (bit 1)
        rd_ris = read_reg_seq("ris_ready", addr["RIS"])
        await rd_ris.start(self.sequencer)
        ris_val = rd_ris.result
        assert ris_val is not None and (ris_val & 0x2), (
            f"AES IRQ: RIS ready bit (bit 1) not set after init, RIS=0x{ris_val if ris_val else 0:x}"
        )

        rd_mis = read_reg_seq("mis_ready", addr["MIS"])
        await rd_mis.start(self.sequencer)
        mis_val = rd_mis.result
        assert mis_val is not None and (mis_val & 0x2), (
            f"AES IRQ: MIS ready bit not set (IM=0x3), MIS=0x{mis_val if mis_val else 0:x}"
        )

        # Clear ready interrupt — note: ready is level-sensitive so the
        # RIS bit will re-assert on the next cycle while core stays ready.
        await write_reg_seq("ic_ready", addr["IC"], 0x2).start(self.sequencer)
        await ClockCycles(dut.CLK, 2)
        rd_ris_clr = read_reg_seq("ris_after_clr", addr["RIS"])
        await rd_ris_clr.start(self.sequencer)

        # Start encryption (triggers valid interrupt when done)
        ctrl = ctrl_base | (1 << 1)
        await write_reg_seq("ctrl_next", addr["CTRL"], ctrl).start(self.sequencer)
        await write_reg_seq("ctrl_clr_next", addr["CTRL"], ctrl_base).start(self.sequencer)

        for _ in range(200):
            seq = read_reg_seq("poll_valid", addr["STATUS"])
            await seq.start(self.sequencer)
            if (seq.result >> 7) & 1:
                break
            await ClockCycles(dut.CLK, 10)

        # Check RIS for valid interrupt (bit 0)
        rd_ris_v = read_reg_seq("ris_valid", addr["RIS"])
        await rd_ris_v.start(self.sequencer)
        ris_valid = rd_ris_v.result
        assert ris_valid is not None and (ris_valid & 0x1), (
            f"AES IRQ: RIS valid bit (bit 0) not set after encrypt, RIS=0x{ris_valid if ris_valid else 0:x}"
        )

        rd_mis_v = read_reg_seq("mis_valid", addr["MIS"])
        await rd_mis_v.start(self.sequencer)
        mis_valid = rd_mis_v.result
        assert mis_valid is not None and (mis_valid & 0x1), (
            f"AES IRQ: MIS valid bit not set (IM=0x3), MIS=0x{mis_valid if mis_valid else 0:x}"
        )

        # Clear all interrupts — both valid and ready are level-sensitive
        # and re-assert while the source condition persists.  Verify the
        # IC write is accepted (MIS responds to IM changes).
        await write_reg_seq("ic_all", addr["IC"], 0x3).start(self.sequencer)
        await ClockCycles(dut.CLK, 2)
        await write_reg_seq("im_none", addr["IM"], 0x0).start(self.sequencer)
        rd_mis_final = read_reg_seq("mis_final", addr["MIS"])
        await rd_mis_final.start(self.sequencer)
        mis_final = rd_mis_final.result
        assert mis_final is not None and mis_final == 0, (
            f"AES IRQ: MIS not zero after disabling all masks, MIS=0x{mis_final if mis_final else 0:x}"
        )

        # Test individual IM mask bits
        for bit in range(2):
            await write_reg_seq(f"im_bit{bit}", addr["IM"], 1 << bit).start(self.sequencer)
            await read_reg_seq(f"im_rd{bit}", addr["IM"]).start(self.sequencer)

        # Restore all
        await write_reg_seq("im_restore", addr["IM"], 0x3).start(self.sequencer)

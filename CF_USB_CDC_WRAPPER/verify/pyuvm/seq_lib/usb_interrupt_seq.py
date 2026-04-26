"""USB CDC interrupt sequence — exercises all interrupt sources, mask, and clear."""

from pyuvm import uvm_sequence, ConfigDB

from cf_verify.bus_env.bus_seq_lib import write_reg_seq, read_reg_seq, reset_seq


class usb_interrupt_seq(uvm_sequence):
    async def body(self):
        await reset_seq("rst").start(self.sequencer)
        regs = ConfigDB().get(None, "", "bus_regs")
        addr = regs.reg_name_to_address

        # Enable all 6 interrupt flags
        if "IM" in addr:
            await write_reg_seq("im_all", addr["IM"], 0x3F).start(self.sequencer)

        # TX full: fill the TX FIFO to capacity
        for i in range(17):
            await write_reg_seq("tx_fill", addr["TXDATA"], i & 0xFF).start(self.sequencer)

        # Read RIS for TX full flag
        if "RIS" in addr:
            await read_reg_seq("ris_txf", addr["RIS"]).start(self.sequencer)

        # Read MIS for masked status
        if "MIS" in addr:
            await read_reg_seq("mis_rd", addr["MIS"]).start(self.sequencer)

        # Clear all interrupts
        if "ICR" in addr:
            await write_reg_seq("ic_clear", addr["ICR"], 0x3F).start(self.sequencer)

        # Verify cleared
        if "RIS" in addr:
            await read_reg_seq("ris_check", addr["RIS"]).start(self.sequencer)

        # Test individual interrupt mask bits
        for bit in range(6):
            if "IM" in addr:
                await write_reg_seq("im_set", addr["IM"], 1 << bit).start(self.sequencer)
            if "IM" in addr:
                await read_reg_seq("im_rd", addr["IM"]).start(self.sequencer)

        # Restore all interrupts
        if "IM" in addr:
            await write_reg_seq("im_all_restore", addr["IM"], 0x3F).start(self.sequencer)

        # Read RIS (TXE and TXB should now be set since FIFO was cleared)
        if "RIS" in addr:
            await read_reg_seq("ris_final", addr["RIS"]).start(self.sequencer)

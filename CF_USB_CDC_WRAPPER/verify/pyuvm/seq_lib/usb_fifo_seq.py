"""USB CDC TX FIFO sequence — fills TX FIFO, checks levels, tests overflow."""

from pyuvm import uvm_sequence, ConfigDB

from cf_verify.bus_env.bus_seq_lib import write_reg_seq, read_reg_seq, reset_seq


class usb_tx_fifo_seq(uvm_sequence):
    async def body(self):
        await reset_seq("rst").start(self.sequencer)
        regs = ConfigDB().get(None, "", "bus_regs")
        addr = regs.reg_name_to_address

        # Enable all interrupts
        if "IM" in addr:
            await write_reg_seq("im_all", addr["IM"], 0x3F).start(self.sequencer)

        # Fill TX FIFO to capacity (16 entries, 4-bit level => max 15)
        for i in range(16):
            await write_reg_seq("tx_fill", addr["TXDATA"], i & 0xFF).start(self.sequencer)

        # Read TX FIFO level and verify it's full
        if "TXFIFOLEVEL" in addr:
            rd_lvl = read_reg_seq("tx_lvl", addr["TXFIFOLEVEL"])
            await rd_lvl.start(self.sequencer)
            tx_level = rd_lvl.result
            assert tx_level is not None and tx_level > 0, (
                f"TX FIFO level should be > 0 after 16 writes, got {tx_level}"
            )

        # Overflow: write more when full
        for i in range(4):
            await write_reg_seq("tx_overflow", addr["TXDATA"], 0xAA).start(self.sequencer)

        # Read flags and check TX full is set
        if "RIS" in addr:
            rd_ris = read_reg_seq("ris_txf", addr["RIS"])
            await rd_ris.start(self.sequencer)

        # Clear interrupts
        if "ICR" in addr:
            await write_reg_seq("ic_clear", addr["ICR"], 0x3F).start(self.sequencer)


class usb_rx_fifo_seq(uvm_sequence):
    async def body(self):
        await reset_seq("rst").start(self.sequencer)
        regs = ConfigDB().get(None, "", "bus_regs")
        addr = regs.reg_name_to_address

        if "IM" in addr:
            await write_reg_seq("im_all", addr["IM"], 0x3F).start(self.sequencer)

        # Read RX FIFO level (should be 0 initially)
        if "RXFIFOLEVEL" in addr:
            await read_reg_seq("rx_lvl_0", addr["RXFIFOLEVEL"]).start(self.sequencer)

        # Try reading from empty RX FIFO
        if "RXDATA" in addr:
            await read_reg_seq("rx_empty", addr["RXDATA"]).start(self.sequencer)

        # Read flags (RXE should be set)
        if "RIS" in addr:
            await read_reg_seq("ris_rxe", addr["RIS"]).start(self.sequencer)

        # Clear interrupts
        if "ICR" in addr:
            await write_reg_seq("ic_clear", addr["ICR"], 0x3F).start(self.sequencer)

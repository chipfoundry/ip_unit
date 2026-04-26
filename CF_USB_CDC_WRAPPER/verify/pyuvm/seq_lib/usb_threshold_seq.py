"""USB CDC threshold sequence — tests TX/RX FIFO threshold configuration."""

from pyuvm import uvm_sequence, ConfigDB

from cf_verify.bus_env.bus_seq_lib import write_reg_seq, read_reg_seq, reset_seq


class usb_threshold_seq(uvm_sequence):
    async def body(self):
        await reset_seq("rst").start(self.sequencer)
        regs = ConfigDB().get(None, "", "bus_regs")
        addr = regs.reg_name_to_address

        if "IM" in addr:
            await write_reg_seq("im_all", addr["IM"], 0x3F).start(self.sequencer)

        # Test various TX FIFO thresholds
        for thr in [1, 4, 8, 12, 15]:
            if "TXFIFOT" in addr:
                await write_reg_seq("tx_thr", addr["TXFIFOT"], thr).start(self.sequencer)
            if "TXFIFOT" in addr:
                await read_reg_seq("tx_thr_rd", addr["TXFIFOT"]).start(self.sequencer)

        # Test various RX FIFO thresholds
        for thr in [1, 4, 8, 12, 15]:
            if "RXFIFOT" in addr:
                await write_reg_seq("rx_thr", addr["RXFIFOT"], thr).start(self.sequencer)
            if "RXFIFOT" in addr:
                await read_reg_seq("rx_thr_rd", addr["RXFIFOT"]).start(self.sequencer)

        # Set TX threshold and fill to trigger below-threshold flag
        if "TXFIFOT" in addr:
            await write_reg_seq("tx_thr_high", addr["TXFIFOT"], 8).start(self.sequencer)

        # Write a few entries (below threshold)
        for i in range(3):
            await write_reg_seq("tx_few", addr["TXDATA"], i).start(self.sequencer)

        # Check TXB (below threshold) flag
        if "RIS" in addr:
            await read_reg_seq("ris_txb", addr["RIS"]).start(self.sequencer)

        # Clear interrupts
        if "ICR" in addr:
            await write_reg_seq("ic_clear", addr["ICR"], 0x3F).start(self.sequencer)

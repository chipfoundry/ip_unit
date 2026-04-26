"""USB CDC coverage closure sequence — systematically exercises all coverage bins."""

from pyuvm import uvm_sequence, ConfigDB

from cf_verify.bus_env.bus_seq_lib import write_reg_seq, read_reg_seq, reset_seq


class usb_coverage_closure_seq(uvm_sequence):
    async def body(self):
        await reset_seq("rst").start(self.sequencer)
        regs = ConfigDB().get(None, "", "bus_regs")
        self.addr = regs.reg_name_to_address

        await self._txdata_bins()
        await self._threshold_sweep()
        await self._fifo_level_sweep()
        await self._flag_exercise()
        await self._interrupt_mask_sweep()

    async def _w(self, name, reg, val):
        await write_reg_seq(name, self.addr[reg], val).start(self.sequencer)

    async def _r(self, name, reg):
        seq = read_reg_seq(name, self.addr[reg])
        await seq.start(self.sequencer)
        return seq.result

    async def _clear(self):
        if "ICR" in self.addr:
            await self._w("ic_clr", "ICR", 0x3F)

    async def _txdata_bins(self):
        """Hit all TX data coverage bins — old 8x32 bins plus new 3-bin override."""
        for bin_idx in range(8):
            val = bin_idx * 32 + 16
            await self._w("tx_bin", "TXDATA", val & 0xFF)

        for val in [0x00, 0x55, 0xAA, 0xFF]:
            await self._w("tx_extra", "TXDATA", val)

    async def _threshold_sweep(self):
        """Sweep all threshold bins for both TX and RX (0, 1-7, 8-15)."""
        for thr in [0, 4, 8, 15]:
            if "TXFIFOT" in self.addr:
                await self._w("tx_thr", "TXFIFOT", thr)
                await self._r("tx_thr_rd", "TXFIFOT")
            if "RXFIFOT" in self.addr:
                await self._w("rx_thr", "RXFIFOT", thr)
                await self._r("rx_thr_rd", "RXFIFOT")

    async def _fifo_level_sweep(self):
        """Fill TX FIFO to various levels and read the level register."""
        await self._clear()

        for fill_to in [1, 4, 8, 12, 15]:
            for i in range(fill_to):
                await self._w("tx_f", "TXDATA", i & 0xFF)

            if "TXFIFOLEVEL" in self.addr:
                await self._r("tx_lvl", "TXFIFOLEVEL")
            if "RXFIFOLEVEL" in self.addr:
                await self._r("rx_lvl", "RXFIFOLEVEL")

        if "TXFIFOLEVEL" in self.addr:
            await self._r("tx_lvl_0", "TXFIFOLEVEL")
        if "RXFIFOLEVEL" in self.addr:
            await self._r("rx_lvl_0", "RXFIFOLEVEL")

    async def _flag_exercise(self):
        """Exercise each RIS flag individually and verify masked interrupts."""
        if "IM" in self.addr:
            await self._w("im_all", "IM", 0x3F)

        # TXE — TX FIFO empty after reset/clear
        await self._clear()
        if "RIS" in self.addr:
            await self._r("ris_txe", "RIS")

        # TXB — set high threshold so level is below it
        if "TXFIFOT" in self.addr:
            await self._w("tx_thr_hi", "TXFIFOT", 14)
        if "RIS" in self.addr:
            await self._r("ris_txb", "RIS")

        # TXF — fill TX FIFO completely to trigger TX Full
        for i in range(16):
            await self._w("tx_fill_full", "TXDATA", i & 0xFF)
        if "RIS" in self.addr:
            await self._r("ris_txf", "RIS")
        if "MIS" in self.addr:
            await self._r("mis_txf", "MIS")

        await self._clear()

        # RXE — RX FIFO should be empty
        if "RIS" in self.addr:
            await self._r("ris_rxe", "RIS")

        # RXA — set low threshold, then read RIS after data arrives via loopback
        if "RXFIFOT" in self.addr:
            await self._w("rx_thr_lo", "RXFIFOT", 1)
        if "RIS" in self.addr:
            await self._r("ris_rxa", "RIS")

        # RXF — read RIS to capture RX Full if loopback fills RX FIFO
        if "RIS" in self.addr:
            await self._r("ris_rxf", "RIS")
        if "MIS" in self.addr:
            await self._r("mis_rxf", "MIS")

        # Read ICR to clear all flags
        await self._clear()
        if "RIS" in self.addr:
            await self._r("ris_post_clr", "RIS")

    async def _interrupt_mask_sweep(self):
        """Toggle each IM bit individually for coverage, read MIS each time."""
        for bit in range(6):
            if "IM" in self.addr:
                await self._w("im_bit", "IM", 1 << bit)
                await self._r("im_rd", "IM")
            if "MIS" in self.addr:
                await self._r("mis_bit", "MIS")

        if "IM" in self.addr:
            await self._w("im_all", "IM", 0x3F)
        if "MIS" in self.addr:
            await self._r("mis_all", "MIS")

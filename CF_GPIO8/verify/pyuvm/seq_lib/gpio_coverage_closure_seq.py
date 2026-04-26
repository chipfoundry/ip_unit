"""GPIO coverage closure — systematically hits all remaining coverage bins."""

from pyuvm import uvm_sequence, ConfigDB
from cocotb.triggers import ClockCycles

from cf_verify.bus_env.bus_seq_lib import write_reg_seq, read_reg_seq, reset_seq


class gpio_coverage_closure_seq(uvm_sequence):
    async def body(self):
        regs = ConfigDB().get(None, "", "bus_regs")
        self.addr = regs.reg_name_to_address
        self.dut = ConfigDB().get(None, "", "DUT")

        await reset_seq("rst").start(self.sequencer)

        if "GCLK" in self.addr:
            await self._w("gclk", "GCLK", 1)

        await self._direction_sweep()
        await self._data_sweep()
        await self._pin_hi_lo_sweep()
        await self._edge_sweep()
        await self._irq_sweep()

    async def _w(self, name, reg, val):
        await write_reg_seq(name, self.addr[reg], val).start(self.sequencer)

    async def _r(self, name, reg):
        await read_reg_seq(name, self.addr[reg]).start(self.sequencer)

    async def _direction_sweep(self):
        """Hit all direction bins: per-pin 0/1 and pattern bins."""
        dirs = [0x00, 0xFF, 0x0F, 0xF0, 0xAA, 0x55, 0x01, 0x80, 0xFE, 0x7F]
        for d in dirs:
            await self._w("dir", "DIR", d)
            await self._r("dir_rd", "DIR")
            await ClockCycles(self.dut.CLK, 3)

    async def _data_sweep(self):
        """Hit all 8 data bins for both IN and OUT (0x00-0x1F .. 0xE0-0xFF)."""
        # Cover all 16 nibbles of DATAO (incl. 0xd0–0xdf bin for reg.DATAO).
        data_reps = [0x08, 0x28, 0x48, 0x68, 0x88, 0xA8, 0xC8, 0xD8, 0xE8]

        await self._w("dir_out", "DIR", 0xFF)
        for d in data_reps:
            await self._w("datao", "DATAO", d)
            await ClockCycles(self.dut.CLK, 3)
            await self._r("datao_rd", "DATAO")

        await self._w("dir_in", "DIR", 0x00)
        for d in data_reps:
            self.dut.io_in.value = d
            await ClockCycles(self.dut.CLK, 5)
            await self._r("datai", "DATAI")

    async def _pin_hi_lo_sweep(self):
        """Trigger pin-high and pin-low RIS flags for all 8 pins."""
        await self._w("dir_in", "DIR", 0x00)

        # Pin high
        for pin in range(8):
            await self._w("ic", "IC", 0xFFFFFFFF)
            self.dut.io_in.value = 1 << pin
            await ClockCycles(self.dut.CLK, 5)
            await self._r("ris_hi", "RIS")

        # Pin low
        for pin in range(8):
            await self._w("ic", "IC", 0xFFFFFFFF)
            self.dut.io_in.value = 0xFF & ~(1 << pin)
            await ClockCycles(self.dut.CLK, 5)
            await self._r("ris_lo", "RIS")

    async def _edge_sweep(self):
        """Generate positive and negative edges on each pin."""
        await self._w("dir_in", "DIR", 0x00)

        # Positive edges
        self.dut.io_in.value = 0x00
        await ClockCycles(self.dut.CLK, 5)
        for pin in range(8):
            await self._w("ic", "IC", 0xFFFFFFFF)
            self.dut.io_in.value = 0x00
            await ClockCycles(self.dut.CLK, 5)
            self.dut.io_in.value = 1 << pin
            await ClockCycles(self.dut.CLK, 5)
            await self._r("ris_pe", "RIS")

        # Negative edges
        self.dut.io_in.value = 0xFF
        await ClockCycles(self.dut.CLK, 5)
        for pin in range(8):
            await self._w("ic", "IC", 0xFFFFFFFF)
            self.dut.io_in.value = 0xFF
            await ClockCycles(self.dut.CLK, 5)
            self.dut.io_in.value = 0xFF & ~(1 << pin)
            await ClockCycles(self.dut.CLK, 5)
            await self._r("ris_ne", "RIS")

    async def _irq_sweep(self):
        """Enable each interrupt source one at a time and trigger it."""
        await self._w("dir_in", "DIR", 0x00)

        # P0HI..P7HI (bits 0-7)
        self.dut.io_in.value = 0x00
        await ClockCycles(self.dut.CLK, 5)
        for pin in range(8):
            await self._w("im", "IM", 1 << pin)
            self.dut.io_in.value = 1 << pin
            await ClockCycles(self.dut.CLK, 5)
            await self._r("mis", "MIS")
            self.dut.io_in.value = 0x00
            await ClockCycles(self.dut.CLK, 3)
            await self._w("ic", "IC", 0xFFFFFFFF)

        # P0LO..P7LO (bits 8-15)
        self.dut.io_in.value = 0xFF
        await ClockCycles(self.dut.CLK, 5)
        for pin in range(8):
            await self._w("im", "IM", 1 << (pin + 8))
            self.dut.io_in.value = 0xFF & ~(1 << pin)
            await ClockCycles(self.dut.CLK, 5)
            await self._r("mis", "MIS")
            self.dut.io_in.value = 0xFF
            await ClockCycles(self.dut.CLK, 3)
            await self._w("ic", "IC", 0xFFFFFFFF)

        # P0PE..P7PE (bits 16-23)
        self.dut.io_in.value = 0x00
        await ClockCycles(self.dut.CLK, 5)
        for pin in range(8):
            await self._w("im", "IM", 1 << (pin + 16))
            self.dut.io_in.value = 1 << pin
            await ClockCycles(self.dut.CLK, 5)
            await self._r("mis", "MIS")
            await self._w("ic", "IC", 0xFFFFFFFF)
            self.dut.io_in.value = 0x00
            await ClockCycles(self.dut.CLK, 3)

        # P0NE..P7NE (bits 24-31)
        self.dut.io_in.value = 0xFF
        await ClockCycles(self.dut.CLK, 5)
        for pin in range(8):
            await self._w("im", "IM", 1 << (pin + 24))
            self.dut.io_in.value = 0xFF & ~(1 << pin)
            await ClockCycles(self.dut.CLK, 5)
            await self._r("mis", "MIS")
            await self._w("ic", "IC", 0xFFFFFFFF)
            self.dut.io_in.value = 0xFF
            await ClockCycles(self.dut.CLK, 3)

        await self._w("im_off", "IM", 0)

"""WDT coverage closure — systematically hits all remaining coverage bins."""

from pyuvm import uvm_sequence, ConfigDB
from cocotb.triggers import ClockCycles

from cf_verify.bus_env.bus_seq_lib import write_reg_seq, read_reg_seq, reset_seq
from seq_lib.wdt_config_seq import wdt_config_seq


class wdt_coverage_closure_seq(uvm_sequence):
    async def body(self):
        await reset_seq("rst").start(self.sequencer)

        regs = ConfigDB().get(None, "", "bus_regs")
        self.addr = regs.reg_name_to_address
        self.dut = ConfigDB().get(None, "", "DUT")

        if "GCLK" in self.addr:
            await self._w("gclk", "GCLK", 1)

        await self._load_value_sweep()
        await self._enable_disable_sweep()
        await self._timeout_sweep()
        await self._irq_sweep()
        await self._timer_value_sweep()

    async def _w(self, name, reg, val):
        await write_reg_seq(name, self.addr[reg], val).start(self.sequencer)

    async def _r(self, name, reg):
        await read_reg_seq(name, self.addr[reg]).start(self.sequencer)

    async def _load_value_sweep(self):
        """Hit all 4 load value bins: zero, tiny, small, large."""
        for load_val in [0x0, 0x55, 0x1000, 0x1000000]:
            await self._w("ctrl_off", "control", 0)
            await self._w("load", "load", load_val)
            await self._r("rd_load", "load")
            await self._r("rd_timer", "timer")

    async def _enable_disable_sweep(self):
        """Hit both enable states."""
        await self._w("load", "load", 0x20)

        await self._w("ctrl_off", "control", 0)
        await self._r("rd_ctrl_off", "control")
        await ClockCycles(self.dut.CLK, 5)
        await self._r("rd_timer_dis", "timer")

        await self._w("ctrl_on", "control", 1)
        await self._r("rd_ctrl_on", "control")
        await ClockCycles(self.dut.CLK, 5)
        await self._r("rd_timer_en", "timer")

        await self._w("ctrl_off2", "control", 0)

    async def _timeout_sweep(self):
        """Generate a timeout and read RIS to hit both timeout flag bins."""
        await self._r("rd_ris_pre", "RIS")

        await self._w("load_small", "load", 0x08)
        await self._w("ctrl_on", "control", 1)
        await ClockCycles(self.dut.CLK, 0x08 + 15)
        await self._r("rd_ris_post", "RIS")
        await self._r("rd_status", "STATUS") if "STATUS" in self.addr else None

        if "IC" in self.addr:
            await self._w("ic_clear", "IC", 0x1)
        if "ICR" in self.addr:
            await self._w("icr_clear", "ICR", 0x1)
        await self._w("ctrl_off", "control", 0)

    async def _irq_sweep(self):
        """Hit all IRQ-related bins: IM masked/unmasked, MIS active/inactive."""
        if "IM" not in self.addr:
            return

        await self._w("im_off", "IM", 0)
        await self._r("rd_im_off", "IM")
        if "MIS" in self.addr:
            await self._r("rd_mis_off", "MIS")

        await self._w("im_on", "IM", 0x1)
        await self._r("rd_im_on", "IM")

        await self._w("load_irq", "load", 0x08)
        await self._w("ctrl_on", "control", 1)
        await ClockCycles(self.dut.CLK, 0x08 + 15)
        if "MIS" in self.addr:
            await self._r("rd_mis_on", "MIS")
        await self._r("rd_ris_irq", "RIS")

        if "IC" in self.addr:
            await self._w("ic_clear", "IC", 0x1)
        if "ICR" in self.addr:
            await self._w("icr_clear", "ICR", 0x1)
        await self._w("im_off2", "IM", 0)
        await self._w("ctrl_off", "control", 0)

    async def _timer_value_sweep(self):
        """Hit timer value bins by reading at different countdown points."""
        for load_val, wait in [(0xFF, 10), (0xFFFF, 10), (0x100000, 10)]:
            await self._w("ctrl_off", "control", 0)
            await self._w("load", "load", load_val)
            await self._w("ctrl_on", "control", 1)
            await ClockCycles(self.dut.CLK, wait)
            await self._r("rd_timer", "timer")
            await self._w("ctrl_off2", "control", 0)

            if "IC" in self.addr:
                await self._w("ic_clear", "IC", 0x1)
            if "ICR" in self.addr:
                await self._w("icr_clear", "ICR", 0x1)

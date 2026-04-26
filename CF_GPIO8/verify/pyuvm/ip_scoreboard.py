"""GPIO8 scoreboard — compares pad outputs against expected register state."""

from cf_verify.base.scoreboard import scoreboard
from ip_item.gpio_item import gpio_item


class gpio_scoreboard(scoreboard):
    def build_phase(self):
        super().build_phase()
        from pyuvm import ConfigDB

        self.check_count = 0
        self.mismatch_count = 0
        self._regs = ConfigDB().get(None, "", "bus_regs")

    def _mirror_bus_write(self, tr):
        """Keep BusRegs in sync with completed bus writes (same as coverage)."""
        from cf_verify.bus_env.bus_item import bus_item

        rname = self._regs._reg_address_to_name.get(tr.addr)
        if not rname:
            return
        if tr.kind == bus_item.WRITE:
            self._regs.write_reg_value(tr.addr, tr.data)

    async def _compare_bus(self):
        """Process bus FIFO first so runtime register image matches pad updates."""
        while True:
            dut_tr = await self.bus_dut_fifo.get()
            ref_tr = await self.bus_ref_fifo.get()
            self._mirror_bus_write(dut_tr)
            self._check("BUS", dut_tr, ref_tr)

    async def _compare_ip(self):
        """Compare gpio_monitor pad outputs against mirrored DIR/DATAO state."""
        from cocotb.triggers import ReadOnly

        while True:
            dut_tr = await self.ip_dut_fifo.get()
            await ReadOnly()
            if dut_tr.is_input:
                continue

            expected_oe = self._regs.read_reg_value("dir") & 0xFF
            expected_out = (self._regs.read_reg_value("datao") & expected_oe) & 0xFF

            actual_oe = dut_tr.direction & 0xFF
            actual_out = (dut_tr.data & actual_oe) & 0xFF

            oe_ok = actual_oe == expected_oe
            out_ok = actual_out == expected_out
            if not oe_ok:
                self.logger.error(
                    f"GPIO OE mismatch: expected 0x{expected_oe:02x}, "
                    f"got 0x{actual_oe:02x}"
                )
            if not out_ok:
                self.logger.error(
                    f"GPIO output mismatch: expected 0x{expected_out:02x}, "
                    f"got 0x{actual_out:02x} (dir=0x{actual_oe:02x})"
                )
            if not (oe_ok and out_ok):
                self.mismatch_count += 1
                self.failed += 1
            self.check_count += 1

    def check_phase(self):
        assert self.failed == 0, (
            f"GPIO scoreboard: bus/IP mismatches failed={self.failed}, passed={self.passed}"
        )
        assert self.mismatch_count == 0, (
            f"GPIO scoreboard pad mismatches: {self.mismatch_count}"
        )

    def report_phase(self):
        self.logger.info(
            f"GPIO8 Scoreboard: {self.check_count} pad checks, "
            f"{self.mismatch_count} mismatches"
        )
        if self.mismatch_count > 0:
            self.logger.error(
                f"GPIO8 Scoreboard FAILED: {self.mismatch_count} mismatches detected"
            )

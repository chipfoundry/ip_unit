"""QSPI scoreboard — compares AHB read data against flash memory reference model."""

from pyuvm import ConfigDB
from cf_verify.base.scoreboard import scoreboard
from cf_verify.bus_env.bus_item import bus_item


class qspi_scoreboard(scoreboard):
    def build_phase(self):
        super().build_phase()
        self.check_count = 0
        self.mismatch_count = 0
        self.flash_memory = None
        self.flash_size = 0
        try:
            self.flash_memory = ConfigDB().get(None, "", "flash_memory")
            self.flash_size = ConfigDB().get(None, "", "flash_size")
        except Exception:
            self.logger.warning("No flash_memory in ConfigDB for scoreboard")

    def _get_expected(self, address):
        """Return expected 32-bit word from flash memory at given address."""
        if self.flash_memory is None or address + 3 >= self.flash_size:
            return 0
        return (
            self.flash_memory[address]
            | (self.flash_memory[address + 1] << 8)
            | (self.flash_memory[address + 2] << 16)
            | (self.flash_memory[address + 3] << 24)
        )

    async def _compare_bus(self):
        """Compare AHB read data against flash memory contents."""
        while True:
            dut_tr = await self.bus_dut_fifo.get()
            ref_tr = await self.bus_ref_fifo.get()

            if dut_tr.kind == bus_item.READ:
                expected = self._get_expected(dut_tr.addr)
                actual = dut_tr.data if dut_tr.data is not None else 0

                if actual != expected:
                    self.mismatch_count += 1
                    self.failed += 1
                    self.logger.error(
                        f"QSPI read mismatch at addr=0x{dut_tr.addr:06x}: "
                        f"expected=0x{expected:08x}, got=0x{actual:08x}"
                    )
                self.check_count += 1

    def check_phase(self):
        assert self.mismatch_count == 0 and self.failed == 0, (
            f"QSPI scoreboard read mismatches: mismatch_count={self.mismatch_count}, "
            f"failed={self.failed}"
        )

    def report_phase(self):
        self.logger.info(
            f"QSPI Scoreboard: {self.check_count} reads checked, "
            f"{self.mismatch_count} mismatches"
        )
        if self.mismatch_count > 0:
            self.logger.error(
                f"QSPI Scoreboard FAILED: {self.mismatch_count} read mismatches"
            )

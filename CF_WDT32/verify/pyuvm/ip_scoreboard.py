"""WDT scoreboard — compares IP monitor events from DUT and reference model."""

from cf_verify.base.scoreboard import scoreboard


class wdt_scoreboard(scoreboard):
    def build_phase(self):
        super().build_phase()
        self.timeout_count = 0

    async def _compare_ip(self):
        """Lockstep compare: each DUT IP transaction has a matching ref prediction."""
        while True:
            dut_tr = await self.ip_dut_fifo.get()
            ref_tr = await self.ip_ref_fifo.get()
            if getattr(dut_tr, "timeout", False):
                self.timeout_count += 1
            self._check("IP", dut_tr, ref_tr)

    def check_phase(self):
        assert self.failed == 0, (
            f"WDT scoreboard mismatches: failed={self.failed}, passed={self.passed}"
        )

    def report_phase(self):
        self.logger.info(
            f"WDT32 Scoreboard: {self.passed} IP matches, {self.failed} mismatches, "
            f"{self.timeout_count} timeout IRQ events observed"
        )

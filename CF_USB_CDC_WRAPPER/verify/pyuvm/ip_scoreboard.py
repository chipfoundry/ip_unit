"""USB CDC scoreboard — compares TX FIFO data and flag assertions."""

from cf_verify.base.scoreboard import scoreboard


class usb_scoreboard(scoreboard):
    def build_phase(self):
        super().build_phase()
        self.check_count = 0

    async def _compare_ip(self):
        """Compare USB CDC transactions from DUT monitor against reference."""
        while True:
            dut_tr = await self.ip_dut_fifo.get()
            ref_tr = await self.ip_ref_fifo.get()
            self.logger.debug(f"USB SB: {dut_tr.convert2string()}")
            self._check("IP", dut_tr, ref_tr)
            self.check_count += 1

    def check_phase(self):
        assert self.failed == 0, (
            f"USB CDC scoreboard mismatches: failed={self.failed}, passed={self.passed}"
        )

    def report_phase(self):
        self.logger.info(
            f"USB CDC Scoreboard: {self.check_count} transactions checked, "
            f"passed={self.passed}, failed={self.failed}"
        )

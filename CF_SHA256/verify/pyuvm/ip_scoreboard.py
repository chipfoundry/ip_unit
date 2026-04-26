"""SHA256 scoreboard — compares DUT digests against reference model."""

from cf_verify.base.scoreboard import scoreboard


class sha256_scoreboard(scoreboard):
    def build_phase(self):
        super().build_phase()
        self.check_count = 0

    async def _compare_ip(self):
        """Compare SHA256 digests from DUT monitor against reference model."""
        while True:
            dut_tr = await self.ip_dut_fifo.get()
            ref_tr = await self.ip_ref_fifo.get()

            self.logger.info(
                f"SHA256 SB: digest=0x{dut_tr.digest:064x} "
                f"ready={dut_tr.ready}"
            )

            self._check("IP", dut_tr, ref_tr)
            self.check_count += 1

    def check_phase(self):
        assert self.failed == 0, (
            f"SHA256 scoreboard mismatches: failed={self.failed}, passed={self.passed}"
        )

    def report_phase(self):
        self.logger.info(
            f"SHA256 Scoreboard: {self.check_count} digests checked, "
            f"passed={self.passed}, failed={self.failed}"
        )

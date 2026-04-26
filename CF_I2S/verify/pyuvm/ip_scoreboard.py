"""I2S scoreboard — compares received I2S samples between DUT and reference."""

from cf_verify.base.scoreboard import scoreboard


class i2s_scoreboard(scoreboard):
    async def _compare_ip(self):
        """Compare received I2S samples from the DUT monitor against the reference model."""
        while True:
            dut_tr = await self.ip_dut_fifo.get()
            ref_tr = await self.ip_ref_fifo.get()
            self._check("IP", dut_tr, ref_tr)

    def check_phase(self):
        assert self.failed == 0, (
            f"I2S scoreboard mismatches: failed={self.failed}, passed={self.passed}"
        )

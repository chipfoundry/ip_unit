"""QSPI coverage component — samples address and cache behavior coverage.

Since this IP has no registers, coverage focuses on:
- AHB read address ranges
- Cache hit/miss behavior
- Flash access patterns
"""

from pyuvm import ConfigDB

from cf_verify.ip_env.ip_coverage import ip_coverage
from ip_coverage.qspi_cov_groups import qspi_cov_groups


class qspi_coverage(ip_coverage):
    def build_phase(self):
        super().build_phase()
        self.cov_groups = qspi_cov_groups("top.ip")

    def sample(self, tr):
        self.cov_groups.sample(tr)

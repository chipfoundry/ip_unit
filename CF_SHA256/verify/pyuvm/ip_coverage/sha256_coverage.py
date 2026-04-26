"""SHA256 coverage component — samples both auto-generated and custom coverage."""

from pyuvm import ConfigDB

from cf_verify.ip_env.ip_coverage import ip_coverage
from ip_coverage.sha256_cov_groups import sha256_cov_groups
from ip_item.sha256_item import sha256_item


class sha256_coverage(ip_coverage):
    def build_phase(self):
        super().build_phase()
        regs = ConfigDB().get(None, "", "bus_regs")
        self.cov_groups = sha256_cov_groups("top.ip", regs)

    def sample(self, tr):
        if isinstance(tr, sha256_item):
            self.cov_groups.sample(tr)
        else:
            self.cov_groups.sample_bus(tr)

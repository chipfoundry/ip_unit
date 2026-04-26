"""AES coverage component — samples both auto-generated and custom coverage."""

from pyuvm import ConfigDB

from cf_verify.ip_env.ip_coverage import ip_coverage
from ip_coverage.aes_cov_groups import aes_cov_groups
from ip_item.aes_item import aes_item


class aes_coverage(ip_coverage):
    def build_phase(self):
        super().build_phase()
        regs = ConfigDB().get(None, "", "bus_regs")
        self.cov_groups = aes_cov_groups("top.ip", regs)

    def sample(self, tr):
        if isinstance(tr, aes_item):
            self.cov_groups.sample(tr)
        else:
            self.cov_groups.sample_bus(tr)

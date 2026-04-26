"""PSRAM coverage component — samples register access coverage."""

from pyuvm import ConfigDB

from cf_verify.ip_env.ip_coverage import ip_coverage
from ip_coverage.psram_cov_groups import psram_cov_groups
from ip_item.psram_item import psram_item


class psram_coverage(ip_coverage):
    def build_phase(self):
        super().build_phase()
        regs = ConfigDB().get(None, "", "bus_regs")
        self.cov_groups = psram_cov_groups("top.ip", regs)

    def sample(self, tr):
        if isinstance(tr, psram_item):
            self.cov_groups.sample(tr)
        else:
            self.cov_groups.sample_bus(tr)

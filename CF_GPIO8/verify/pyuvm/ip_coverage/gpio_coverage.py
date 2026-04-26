"""GPIO coverage component — samples both auto-generated and custom coverage."""

from pyuvm import ConfigDB

from cf_verify.ip_env.ip_coverage import ip_coverage
from ip_coverage.gpio_cov_groups import gpio_cov_groups
from ip_item.gpio_item import gpio_item


class gpio_coverage(ip_coverage):
    def build_phase(self):
        super().build_phase()
        regs = ConfigDB().get(None, "", "bus_regs")
        self.cov_groups = gpio_cov_groups("top.ip", regs)

    def sample(self, tr):
        if isinstance(tr, gpio_item):
            self.cov_groups.sample(tr)
        else:
            self.cov_groups.sample_bus(tr)

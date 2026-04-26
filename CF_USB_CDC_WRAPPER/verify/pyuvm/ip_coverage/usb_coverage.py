"""USB CDC coverage component — samples both auto-generated and custom coverage."""

from pyuvm import ConfigDB

from cf_verify.ip_env.ip_coverage import ip_coverage
from ip_coverage.usb_cov_groups import usb_cov_groups
from ip_item.usb_item import usb_item


class usb_coverage(ip_coverage):
    def build_phase(self):
        super().build_phase()
        regs = ConfigDB().get(None, "", "bus_regs")
        self.cov_groups = usb_cov_groups("top.ip", regs)

    def sample(self, tr):
        if isinstance(tr, usb_item):
            self.cov_groups.sample(tr)
        else:
            self.cov_groups.sample_bus(tr)

"""AES coverage groups — auto-generated register coverage + AES-specific bins."""

from cocotb_coverage.coverage import CoverPoint, CoverCross

from cf_verify.coverage.auto_coverage import generate_coverage_from_yaml
from cf_verify.bus_env.bus_item import bus_item
from ip_item.aes_item import aes_item


AES_FIELD_BINS = {
    ("CTRL", "encdec_reg"): [(0, 0), (1, 1)],
    ("CTRL", "keylen_reg"): [(0, 0), (1, 1)],
    ("CTRL", "init_reg"):   [(0, 0), (1, 1)],
    ("CTRL", "next_reg"):   [(0, 0), (1, 1)],
    ("STATUS", "ready_reg"): [(0, 0), (1, 1)],
    ("STATUS", "valid_reg"): [(0, 0), (1, 1)],
    ("KEY0", None): [(0, 0), (1, 0xFFFFFFFF)],
    ("KEY1", None): [(0, 0), (1, 0xFFFFFFFF)],
    ("KEY2", None): [(0, 0), (1, 0xFFFFFFFF)],
    ("KEY3", None): [(0, 0), (1, 0xFFFFFFFF)],
    ("KEY4", None): [(0, 0), (1, 0xFFFFFFFF)],
    ("KEY5", None): [(0, 0), (1, 0xFFFFFFFF)],
    ("KEY6", None): [(0, 0), (1, 0xFFFFFFFF)],
    ("KEY7", None): [(0, 0), (1, 0xFFFFFFFF)],
    ("BLOCK0", None): [(0, 0), (1, 0xFFFFFFFF)],
    ("BLOCK1", None): [(0, 0), (1, 0xFFFFFFFF)],
    ("BLOCK2", None): [(0, 0), (1, 0xFFFFFFFF)],
    ("BLOCK3", None): [(0, 0), (1, 0xFFFFFFFF)],
    ("RESULT0", None): [(0, 0), (1, 0xFFFFFFFF)],
    ("RESULT1", None): [(0, 0), (1, 0xFFFFFFFF)],
    ("RESULT2", None): [(0, 0), (1, 0xFFFFFFFF)],
    ("RESULT3", None): [(0, 0), (1, 0xFFFFFFFF)],
}


class aes_cov_groups:
    def __init__(self, hierarchy, regs):
        self.hierarchy = hierarchy
        self.regs = regs

        self.auto_points = generate_coverage_from_yaml(
            regs, hierarchy, field_bins_override=AES_FIELD_BINS,
        )

        self.custom_cov = self._aes_custom_coverage()
        self._init_sample(None)

    def _init_sample(self, tr):
        """Cold-start: register all CoverPoints without counting."""
        @self._apply_decorators(self.auto_points + self.custom_cov)
        def _cold(tr):
            pass

    def sample(self, tr):
        """Sample using an aes_item."""
        @self._apply_decorators(self.auto_points + self.custom_cov)
        def _s(tr):
            pass
        _s(tr)

    def sample_bus(self, tr):
        """Sample from bus transactions — update register shadows on reads."""
        if tr.kind == bus_item.READ:
            rname = self.regs._reg_address_to_name.get(tr.addr)
            if rname:
                self.regs._reg_values[rname.lower()] = tr.data

        if tr.kind == bus_item.WRITE:
            rname = self.regs._reg_address_to_name.get(tr.addr)
            if rname:
                self.regs._reg_values[rname.lower()] = tr.data

        @self._apply_decorators(self.auto_points + self.custom_cov)
        def _bus(tr):
            pass
        _bus(tr)

    def _aes_custom_coverage(self):
        h = self.hierarchy
        regs = self.regs
        return [
            CoverPoint(
                f"{h}.KeyLength",
                xf=lambda tr: (regs.read_reg_value("CTRL") >> 3) & 1,
                bins=[0, 1],
                bins_labels=["aes_128", "aes_256"],
                at_least=1,
            ),
            CoverPoint(
                f"{h}.EncDec",
                xf=lambda tr: (regs.read_reg_value("CTRL") >> 2) & 1,
                bins=[0, 1],
                bins_labels=["decrypt", "encrypt"],
                at_least=1,
            ),
            CoverPoint(
                f"{h}.ResultValid",
                xf=lambda tr: (regs.read_reg_value("STATUS") >> 7) & 1
                    if "STATUS" in regs._reg_values else 0,
                bins=[0, 1],
                bins_labels=["not_valid", "valid"],
                at_least=1,
            ),
            CoverPoint(
                f"{h}.Ready",
                xf=lambda tr: (regs.read_reg_value("STATUS") >> 6) & 1
                    if "STATUS" in regs._reg_values else 0,
                bins=[0, 1],
                bins_labels=["not_ready", "ready"],
                at_least=1,
            ),
            CoverCross(
                f"{h}.KeyLen_x_EncDec",
                items=[f"{h}.KeyLength", f"{h}.EncDec"],
            ),
            CoverPoint(
                f"{h}.IRQ.RIS_valid",
                xf=lambda tr: regs.read_reg_value("RIS") & 1
                    if "RIS" in regs._reg_values else 0,
                bins=[0, 1],
                bins_labels=["no_valid_irq", "valid_irq"],
                at_least=1,
            ),
            CoverPoint(
                f"{h}.IRQ.RIS_ready",
                xf=lambda tr: (regs.read_reg_value("RIS") >> 1) & 1
                    if "RIS" in regs._reg_values else 0,
                bins=[0, 1],
                bins_labels=["no_ready_irq", "ready_irq"],
                at_least=1,
            ),
        ]

    @staticmethod
    def _apply_decorators(decorators):
        def wrapper(func):
            for dec in decorators:
                func = dec(func)
            return func
        return wrapper

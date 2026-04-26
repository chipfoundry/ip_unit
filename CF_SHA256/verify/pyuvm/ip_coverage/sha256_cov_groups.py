"""SHA256 coverage groups — auto-generated register coverage + SHA256-specific bins."""

from cocotb_coverage.coverage import CoverPoint, CoverCross

from cf_verify.coverage.auto_coverage import generate_coverage_from_yaml
from cf_verify.bus_env.bus_item import bus_item
from ip_item.sha256_item import sha256_item


SHA256_FIELD_BINS = {
    ("CTRL", "init_reg"): [(0, 0), (1, 1)],
    ("CTRL", "next_reg"): [(0, 0), (1, 1)],
    ("CTRL", "mode_reg"): [(0, 0), (1, 1)],
    ("STATUS", "ready_reg"): [(0, 0), (1, 1)],
    ("STATUS", "digest_valid_reg"): [(0, 0), (1, 1)],
    ("BLOCK0", None): [(0, 0), (1, 0xFFFFFFFF)],
    ("BLOCK1", None): [(0, 0), (1, 0xFFFFFFFF)],
    ("BLOCK2", None): [(0, 0), (1, 0xFFFFFFFF)],
    ("BLOCK3", None): [(0, 0), (1, 0xFFFFFFFF)],
    ("BLOCK4", None): [(0, 0), (1, 0xFFFFFFFF)],
    ("BLOCK5", None): [(0, 0), (1, 0xFFFFFFFF)],
    ("BLOCK6", None): [(0, 0), (1, 0xFFFFFFFF)],
    ("BLOCK7", None): [(0, 0), (1, 0xFFFFFFFF)],
    ("BLOCK8", None): [(0, 0), (1, 0xFFFFFFFF)],
    ("BLOCK9", None): [(0, 0), (1, 0xFFFFFFFF)],
    ("BLOCK10", None): [(0, 0), (1, 0xFFFFFFFF)],
    ("BLOCK11", None): [(0, 0), (1, 0xFFFFFFFF)],
    ("BLOCK12", None): [(0, 0), (1, 0xFFFFFFFF)],
    ("BLOCK13", None): [(0, 0), (1, 0xFFFFFFFF)],
    ("BLOCK14", None): [(0, 0), (1, 0xFFFFFFFF)],
    ("BLOCK15", None): [(0, 0), (1, 0xFFFFFFFF)],
    ("DIGEST0", None): [(0, 0), (1, 0xFFFFFFFF)],
    ("DIGEST1", None): [(0, 0), (1, 0xFFFFFFFF)],
    ("DIGEST2", None): [(0, 0), (1, 0xFFFFFFFF)],
    ("DIGEST3", None): [(0, 0), (1, 0xFFFFFFFF)],
    ("DIGEST4", None): [(0, 0), (1, 0xFFFFFFFF)],
    ("DIGEST5", None): [(0, 0), (1, 0xFFFFFFFF)],
    ("DIGEST6", None): [(0, 0), (1, 0xFFFFFFFF)],
    ("DIGEST7", None): [(0, 0), (1, 0xFFFFFFFF)],
}


class sha256_cov_groups:
    def __init__(self, hierarchy, regs):
        self.hierarchy = hierarchy
        self.regs = regs

        self.auto_points = generate_coverage_from_yaml(
            regs, hierarchy, field_bins_override=SHA256_FIELD_BINS,
            skip_crosses=True,
        )

        self.custom_cov = self._sha256_custom_coverage()
        self._init_sample(None)

    def _init_sample(self, tr):
        @self._apply_decorators(self.auto_points + self.custom_cov)
        def _cold(tr):
            pass

    def sample(self, tr):
        @self._apply_decorators(self.auto_points + self.custom_cov)
        def _s(tr):
            pass
        _s(tr)

    def sample_bus(self, tr):
        rname = self.regs._reg_address_to_name.get(tr.addr)
        if rname:
            if tr.kind == bus_item.WRITE:
                self.regs._reg_values[rname.lower()] = tr.data
            elif tr.kind == bus_item.READ:
                reg = next(
                    (r for r in self.regs._registers if r.name == rname),
                    None,
                )
                if not reg or reg.mode != "w":
                    self.regs._reg_values[rname.lower()] = tr.data

        @self._apply_decorators(self.auto_points + self.custom_cov)
        def _bus(tr):
            pass
        _bus(tr)

    def _sha256_custom_coverage(self):
        h = self.hierarchy
        regs = self.regs
        return [
            CoverPoint(
                f"{h}.HashMode",
                xf=lambda tr: (regs.read_reg_value("CTRL") >> 2) & 1
                if regs.read_reg_value("CTRL") is not None else -1,
                bins=[0, 1],
                bins_labels=["sha224", "sha256"],
                at_least=1,
            ),
            CoverPoint(
                f"{h}.DigestValid",
                xf=lambda tr: (regs.read_reg_value("STATUS") >> 7) & 1
                if regs.read_reg_value("STATUS") is not None else -1,
                bins=[0, 1],
                bins_labels=["not_valid", "valid"],
                at_least=1,
            ),
            CoverPoint(
                f"{h}.Ready",
                xf=lambda tr: (regs.read_reg_value("STATUS") >> 6) & 1
                if regs.read_reg_value("STATUS") is not None else -1,
                bins=[0, 1],
                bins_labels=["not_ready", "ready"],
                at_least=1,
            ),
            CoverPoint(
                f"{h}.IRQ.RIS_valid",
                xf=lambda tr: regs.read_reg_value("RIS") & 1
                if regs.read_reg_value("RIS") is not None else -1,
                bins=[0, 1],
                bins_labels=["no_valid_irq", "valid_irq"],
                at_least=1,
            ),
            CoverPoint(
                f"{h}.IRQ.RIS_ready",
                xf=lambda tr: (regs.read_reg_value("RIS") >> 1) & 1
                if regs.read_reg_value("RIS") is not None else -1,
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

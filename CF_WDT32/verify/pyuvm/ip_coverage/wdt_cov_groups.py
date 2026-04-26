"""WDT coverage groups — auto-generated + WDT-specific custom coverage."""

from cocotb_coverage.coverage import CoverPoint, CoverCross

from cf_verify.coverage.auto_coverage import generate_coverage_from_yaml
from cf_verify.bus_env.bus_item import bus_item
from ip_item.wdt_item import wdt_item

LOAD_BINS = [
    (0x00000000, 0x000000FF),
    (0x00000100, 0x0000FFFF),
    (0x00010000, 0x00FFFFFF),
    (0x01000000, 0xFFFFFFFF),
]

TIMER_BINS = [
    (0x00000000, 0x000000FF),
    (0x00000100, 0x0000FFFF),
    (0x00010000, 0x00FFFFFF),
    (0x01000000, 0xFFFFFFFF),
]


WDT_FIELD_BINS = {
    ("timer", None): [(0, 0), (1, 255), (256, 0xFFFF), (0x10000, 0xFFFFFFFF)],
    ("load", None): [(0, 0), (1, 255), (256, 0xFFFF), (0x10000, 0xFFFFFFFF)],
    ("control", None): [(0, 0), (1, 1)],
}


class wdt_cov_groups:
    def __init__(self, hierarchy, regs):
        self.hierarchy = hierarchy
        self.regs = regs

        self.auto_points = generate_coverage_from_yaml(
            regs, hierarchy,
            field_bins_override=WDT_FIELD_BINS,
        )

        self.load_cov = self._load_coverage()
        self.timer_cov = self._timer_coverage()
        self.control_cov = self._control_coverage()
        self.timeout_cov = self._timeout_coverage()
        self.irq_cov = self._irq_coverage()

        self._init_sample(None)

    def _init_sample(self, tr):
        """Cold-start: register all CoverPoints without actually counting."""
        @self._apply_decorators(
            self.auto_points + self.load_cov + self.timer_cov
            + self.control_cov + self.timeout_cov + self.irq_cov
        )
        def _cold(tr):
            pass

    def sample(self, tr):
        """Sample everything using a wdt_item."""
        @self._apply_decorators(
            self.auto_points + self.load_cov + self.timer_cov
            + self.control_cov + self.timeout_cov + self.irq_cov
        )
        def _s(tr):
            pass
        _s(tr)

    def sample_bus(self, tr):
        """Sample from bus transactions; update register values."""
        rname = self.regs._reg_address_to_name.get(tr.addr)
        if rname:
            self.regs._reg_values[rname.lower()] = tr.data

        @self._apply_decorators(
            self.auto_points + self.load_cov + self.timer_cov
            + self.control_cov + self.timeout_cov + self.irq_cov
        )
        def _bus(tr):
            pass
        _bus(tr)

    def _load_coverage(self):
        return [CoverPoint(
            f"{self.hierarchy}.Load_Value",
            xf=lambda tr: self.regs.read_reg_value("load"),
            bins=LOAD_BINS,
            bins_labels=[
                "tiny_0x00-0xFF",
                "small_0x100-0xFFFF",
                "medium_0x10000-0xFFFFFF",
                "large_0x1000000-0xFFFFFFFF",
            ],
            rel=lambda val, b: b[0] <= val <= b[1],
            at_least=1,
        )]

    def _timer_coverage(self):
        return [CoverPoint(
            f"{self.hierarchy}.Timer_Value",
            xf=lambda tr: self.regs.read_reg_value("timer"),
            bins=TIMER_BINS,
            bins_labels=[
                "tiny_0x00-0xFF",
                "small_0x100-0xFFFF",
                "medium_0x10000-0xFFFFFF",
                "large_0x1000000-0xFFFFFFFF",
            ],
            rel=lambda val, b: b[0] <= val <= b[1],
            at_least=1,
        )]

    def _control_coverage(self):
        return [CoverPoint(
            f"{self.hierarchy}.WDT_Enable",
            xf=lambda tr: self.regs.read_reg_value("control") & 1,
            bins=[0, 1],
            bins_labels=["disabled", "enabled"],
            at_least=1,
        )]

    def _timeout_coverage(self):
        return [CoverPoint(
            f"{self.hierarchy}.Timeout_Flag",
            xf=lambda tr: self.regs.read_reg_value("RIS") & 1,
            bins=[0, 1],
            bins_labels=["no_timeout", "timeout"],
            at_least=1,
        )]

    def _irq_coverage(self):
        return [
            CoverPoint(
                f"{self.hierarchy}.IRQ.IM",
                xf=lambda tr: self.regs.read_reg_value("IM") & 1,
                bins=[0, 1],
                bins_labels=["masked", "unmasked"],
                at_least=1,
            ),
            CoverPoint(
                f"{self.hierarchy}.IRQ.MIS",
                xf=lambda tr: self.regs.read_reg_value("MIS") & 1,
                bins=[0, 1],
                bins_labels=["no_irq", "irq_active"],
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

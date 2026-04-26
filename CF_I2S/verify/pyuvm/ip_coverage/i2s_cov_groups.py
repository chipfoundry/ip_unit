"""I2S coverage groups — auto-generated + I2S-specific custom coverage."""

from cocotb_coverage.coverage import CoverPoint, CoverCross

from cf_verify.coverage.auto_coverage import generate_coverage_from_yaml
from cf_verify.bus_env.bus_item import bus_item
from ip_item.i2s_item import i2s_item

I2S_FIELD_BINS = {
    ("CFG", "channels"): [(1, 1), (2, 2), (3, 3)],
    ("CFG", "sample_size"): [(v, v) for v in [8, 16, 24, 32]],
    ("PR", None): [(0, 3), (4, 15), (16, 63), (64, 255)],
}


class i2s_cov_groups:
    def __init__(self, hierarchy, regs):
        self.hierarchy = hierarchy
        self.regs = regs

        self.rxdata_addr = regs.reg_name_to_address.get("RXDATA")

        self.auto_points = generate_coverage_from_yaml(
            regs, hierarchy, field_bins_override=I2S_FIELD_BINS,
        )

        self.channel_cov = self._channel_coverage()
        self.sample_size_cov = self._sample_size_coverage()
        self.fifo_cov = self._fifo_coverage()
        self.flag_cov = self._flag_coverage()
        self.mode_cov = self._mode_coverage()

        self._init_sample(None)

    def _init_sample(self, tr):
        @self._apply_decorators(
            self.auto_points + self.channel_cov + self.sample_size_cov
            + self.fifo_cov + self.flag_cov + self.mode_cov
        )
        def _cold(tr):
            pass

    def sample(self, tr):
        @self._apply_decorators(
            self.auto_points + self.channel_cov + self.sample_size_cov
            + self.fifo_cov + self.flag_cov + self.mode_cov
        )
        def _s(tr):
            pass
        _s(tr)

    def sample_bus(self, tr):
        rname = self.regs._reg_address_to_name.get(tr.addr)
        if rname:
            self.regs._reg_values[rname.lower()] = tr.data

        @self._apply_decorators(
            self.auto_points + self.fifo_cov + self.flag_cov + self.mode_cov
        )
        def _bus(tr):
            pass
        _bus(tr)

        if (self.rxdata_addr is not None
                and tr.addr == self.rxdata_addr
                and tr.kind == bus_item.READ):
            self.sample(self._synth(tr.data))

    def _synth(self, data):
        cfg = self.regs.read_reg_value("CFG")
        sample_size = ((cfg >> 4) & 0x3F) or 32
        channels = cfg & 0x3

        item = i2s_item("synth")
        item.sample_data = data & ((1 << sample_size) - 1)
        item.sample_size = sample_size
        if channels == 1:
            item.channel = i2s_item.RIGHT
        else:
            item.channel = i2s_item.LEFT
        return item

    def _channel_coverage(self):
        return [
            CoverPoint(
                f"{self.hierarchy}.Channel",
                xf=lambda tr: self.regs.read_reg_value("CFG") & 0x3,
                bins=[1, 2, 3],
                bins_labels=["right", "left", "stereo"],
                at_least=1,
            ),
        ]

    def _sample_size_coverage(self):
        return [
            CoverPoint(
                f"{self.hierarchy}.SampleSize",
                xf=lambda tr: (self.regs.read_reg_value("CFG") >> 4) & 0x3F,
                bins=[(8, 8), (16, 16), (24, 24), (32, 32)],
                bins_labels=["8bit", "16bit", "24bit", "32bit"],
                at_least=1,
                rel=lambda val, b: b[0] <= val <= b[1],
            ),
        ]

    def _fifo_coverage(self):
        return [
            CoverPoint(
                f"{self.hierarchy}.FIFO.Empty",
                xf=lambda tr: self.regs.read_reg_value("RIS") & 1,
                bins=[0, 1], bins_labels=["not_empty", "empty"],
                at_least=1,
            ),
            CoverPoint(
                f"{self.hierarchy}.FIFO.Above",
                xf=lambda tr: (self.regs.read_reg_value("RIS") >> 1) & 1,
                bins=[0, 1], bins_labels=["below", "above"],
                at_least=1,
            ),
            CoverPoint(
                f"{self.hierarchy}.FIFO.Full",
                xf=lambda tr: (self.regs.read_reg_value("RIS") >> 2) & 1,
                bins=[0, 1], bins_labels=["not_full", "full"],
                at_least=1,
            ),
        ]

    def _flag_coverage(self):
        return [
            CoverPoint(
                f"{self.hierarchy}.Flags.AVGF",
                xf=lambda tr: (self.regs.read_reg_value("RIS") >> 3) & 1,
                bins=[0, 1], bins_labels=["no_avg", "avg"],
                at_least=1,
            ),
            CoverPoint(
                f"{self.hierarchy}.Flags.ZCRF",
                xf=lambda tr: (self.regs.read_reg_value("RIS") >> 4) & 1,
                bins=[0, 1], bins_labels=["no_zcr", "zcr"],
                at_least=1,
            ),
            CoverPoint(
                f"{self.hierarchy}.Flags.VADF",
                xf=lambda tr: (self.regs.read_reg_value("RIS") >> 5) & 1,
                bins=[0, 1], bins_labels=["no_vad", "vad"],
                at_least=1,
            ),
        ]

    def _mode_coverage(self):
        return [
            CoverPoint(
                f"{self.hierarchy}.SignExtend",
                xf=lambda tr: (self.regs.read_reg_value("CFG") >> 2) & 1,
                bins=[0, 1], bins_labels=["no_sign_ext", "sign_ext"],
                at_least=1,
            ),
            CoverPoint(
                f"{self.hierarchy}.LeftJustified",
                xf=lambda tr: (self.regs.read_reg_value("CFG") >> 3) & 1,
                bins=[0, 1], bins_labels=["standard", "left_justified"],
                at_least=1,
            ),
            CoverPoint(
                f"{self.hierarchy}.Prescaler",
                xf=lambda tr: self.regs.read_reg_value("PR"),
                bins=[(0, 3), (4, 15), (16, 63), (64, 255)],
                bins_labels=["low", "med", "high", "very_high"],
                at_least=1,
                rel=lambda val, b: b[0] <= val <= b[1],
            ),
        ]

    @staticmethod
    def _apply_decorators(decorators):
        def wrapper(func):
            for dec in decorators:
                func = dec(func)
            return func
        return wrapper

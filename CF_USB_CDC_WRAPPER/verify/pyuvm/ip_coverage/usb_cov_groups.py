"""USB CDC coverage groups — register and FIFO-level coverage."""

from cocotb_coverage.coverage import CoverPoint, CoverCross

from cf_verify.coverage.auto_coverage import generate_coverage_from_yaml
from cf_verify.bus_env.bus_item import bus_item
from ip_item.usb_item import usb_item

TXDATA_BINS = [(0, 0), (1, 127), (128, 255)]
TX_LEVEL_BINS = [(0, 0), (1, 7), (8, 15)]
THRESHOLD_BINS = [(0, 0), (1, 7), (8, 15)]

USB_FIELD_BINS = {
    ("TXDATA", None): [(0, 0), (1, 127), (128, 255)],
    ("RXDATA", None): [(0, 0), (1, 127), (128, 255)],
    ("TXFIFOLEVEL", None): [(0, 0), (1, 7), (8, 15)],
    ("RXFIFOLEVEL", None): [(0, 0), (1, 7), (8, 15)],
    ("TXFIFOT", None): [(0, 0), (1, 7), (8, 15)],
    ("RXFIFOT", None): [(0, 0), (1, 7), (8, 15)],
}


class usb_cov_groups:
    def __init__(self, hierarchy, regs):
        self.hierarchy = hierarchy
        self.regs = regs

        self.txdata_addr = regs.reg_name_to_address.get("TXDATA")
        self.rxdata_addr = regs.reg_name_to_address.get("RXDATA")

        self.auto_points = generate_coverage_from_yaml(
            regs, hierarchy, field_bins_override=USB_FIELD_BINS,
        )

        self.fifo_cov = self._fifo_coverage()
        self.flag_cov = self._flag_coverage()

        self._init_sample(None)

    def _init_sample(self, tr):
        """Cold-start: register all CoverPoints without actually counting."""
        @self._apply_decorators(
            self.auto_points + self.fifo_cov + self.flag_cov
        )
        def _cold(tr):
            pass

    def sample(self, tr):
        """Sample everything using a usb_item."""
        @self._apply_decorators(
            self.auto_points + self.fifo_cov + self.flag_cov
        )
        def _s(tr):
            pass
        _s(tr)

    def sample_bus(self, tr):
        """Sample from bus transactions."""
        rname = self.regs._reg_address_to_name.get(tr.addr)
        if rname:
            self.regs._reg_values[rname.lower()] = tr.data

        @self._apply_decorators(self.auto_points + self.fifo_cov + self.flag_cov)
        def _bus(tr):
            pass
        _bus(tr)

        if (self.txdata_addr is not None
                and tr.addr == self.txdata_addr
                and tr.kind == bus_item.WRITE):
            item = usb_item("synth_tx")
            item.direction = usb_item.TX
            item.data = tr.data & 0xFF
            self.sample(item)
        elif (self.rxdata_addr is not None
              and tr.addr == self.rxdata_addr
              and tr.kind == bus_item.READ):
            item = usb_item("synth_rx")
            item.direction = usb_item.RX
            item.data = tr.data & 0xFF
            self.sample(item)

    def _fifo_coverage(self):
        points = []
        points.append(CoverPoint(
            f"{self.hierarchy}.TX.Data",
            xf=lambda tr: (
                tr.data if isinstance(tr, usb_item)
                and tr.direction == usb_item.TX
                else -1
            ),
            bins=TXDATA_BINS,
            bins_labels=[f"0x{lo:02x}-0x{hi:02x}" for lo, hi in TXDATA_BINS],
            rel=lambda val, b: b[0] <= val <= b[1],
        ))

        points.append(CoverPoint(
            f"{self.hierarchy}.TXFIFO.Level",
            xf=lambda tr: self.regs.read_reg_value("TXFIFOLEVEL"),
            bins=TX_LEVEL_BINS,
            bins_labels=[f"{lo}-{hi}" for lo, hi in TX_LEVEL_BINS],
            rel=lambda val, b: b[0] <= val <= b[1],
        ))

        points.append(CoverPoint(
            f"{self.hierarchy}.TXFIFOT.Value",
            xf=lambda tr: self.regs.read_reg_value("TXFIFOT"),
            bins=THRESHOLD_BINS,
            bins_labels=[f"{lo}-{hi}" for lo, hi in THRESHOLD_BINS],
            rel=lambda val, b: b[0] <= val <= b[1],
        ))
        points.append(CoverPoint(
            f"{self.hierarchy}.RXFIFOT.Value",
            xf=lambda tr: self.regs.read_reg_value("RXFIFOT"),
            bins=THRESHOLD_BINS,
            bins_labels=[f"{lo}-{hi}" for lo, hi in THRESHOLD_BINS],
            rel=lambda val, b: b[0] <= val <= b[1],
        ))

        return points

    def _flag_coverage(self):
        tx_flags = [
            ("TXE", 0, "TX Empty"),
            ("TXB", 1, "TX Below Threshold"),
            ("TXF", 5, "TX Full"),
        ]
        points = []
        for name, bit, desc in tx_flags:
            points.append(CoverPoint(
                f"{self.hierarchy}.Flags.{name}",
                xf=lambda tr, b=bit: (self.regs.read_reg_value("RIS") >> b) & 1
                if self.regs.read_reg_value("RIS") is not None else -1,
                bins=[0, 1],
                bins_labels=[f"no_{name}", name],
                at_least=1,
            ))
        return points

    @staticmethod
    def _apply_decorators(decorators):
        def wrapper(func):
            for dec in decorators:
                func = dec(func)
            return func
        return wrapper

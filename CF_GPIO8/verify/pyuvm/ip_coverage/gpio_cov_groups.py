"""GPIO coverage groups — auto-generated + GPIO-specific custom coverage."""

from cocotb_coverage.coverage import CoverPoint, CoverCross

from cf_verify.coverage.auto_coverage import generate_coverage_from_yaml
from cf_verify.bus_env.bus_item import bus_item
from ip_item.gpio_item import gpio_item

DATAO_BINS = [(i * 32, i * 32 + 31) for i in range(8)]
DIR_BINS = [0x00, 0x0F, 0xF0, 0xFF]


class gpio_cov_groups:
    def __init__(self, hierarchy, regs):
        self.hierarchy = hierarchy
        self.regs = regs

        self.datai_addr = regs.reg_name_to_address.get("DATAI")
        self.datao_addr = regs.reg_name_to_address.get("DATAO")
        self.dir_addr = regs.reg_name_to_address.get("DIR")

        self.auto_points = generate_coverage_from_yaml(regs, hierarchy)

        self.direction_cov = self._direction_coverage()
        self.data_cov = self._data_coverage()
        self.pin_hi_lo_cov = self._pin_hi_lo_coverage()
        self.edge_cov = self._edge_coverage()
        self.irq_cov = self._irq_coverage()

        self._init_sample(None)

    def _init_sample(self, tr):
        @self._apply_decorators(
            self.auto_points + self.direction_cov + self.data_cov
            + self.pin_hi_lo_cov + self.edge_cov + self.irq_cov
        )
        def _cold(tr):
            pass

    def sample(self, tr):
        @self._apply_decorators(
            self.auto_points + self.direction_cov + self.data_cov
            + self.pin_hi_lo_cov + self.edge_cov + self.irq_cov
        )
        def _s(tr):
            pass
        _s(tr)

    def sample_bus(self, tr):
        rname = self.regs._reg_address_to_name.get(tr.addr)
        if rname:
            if tr.kind == bus_item.WRITE:
                self.regs._reg_values[rname.lower()] = tr.data
            elif tr.kind == bus_item.READ:
                self.regs._reg_values[rname.lower()] = tr.data

        @self._apply_decorators(
            self.auto_points + self.direction_cov
            + self.pin_hi_lo_cov + self.edge_cov + self.irq_cov
        )
        def _bus(tr):
            pass
        _bus(tr)

        if (self.datao_addr is not None
                and tr.addr == self.datao_addr
                and tr.kind == bus_item.WRITE):
            self.sample(self._synth_output(tr.data))
        elif (self.datai_addr is not None
              and tr.addr == self.datai_addr
              and tr.kind == bus_item.READ):
            self.sample(self._synth_input(tr.data))

    def _synth_output(self, data):
        item = gpio_item("synth_out")
        item.data = data & 0xFF
        item.direction = self.regs.read_reg_value("DIR")
        item.is_input = False
        return item

    def _synth_input(self, data):
        item = gpio_item("synth_in")
        item.data = data & 0xFF
        item.direction = self.regs.read_reg_value("DIR")
        item.is_input = True
        return item

    def _direction_coverage(self):
        points = []
        for bit in range(8):
            points.append(CoverPoint(
                f"{self.hierarchy}.DIR.pin{bit}",
                xf=lambda tr, b=bit: (self.regs.read_reg_value("DIR") >> b) & 1,
                bins=[0, 1],
                bins_labels=["input", "output"],
                at_least=1,
            ))
        points.append(CoverPoint(
            f"{self.hierarchy}.DIR.Pattern",
            xf=lambda tr: self.regs.read_reg_value("DIR"),
            bins=DIR_BINS,
            bins_labels=["all_in", "lo_out", "hi_out", "all_out"],
            at_least=1,
        ))
        return points

    def _data_coverage(self):
        points = []
        for io_type in [gpio_item.INPUT, gpio_item.OUTPUT]:
            d_str = "IN" if io_type == gpio_item.INPUT else "OUT"
            is_in = io_type == gpio_item.INPUT
            points.append(CoverPoint(
                f"{self.hierarchy}.Data.{d_str}",
                xf=lambda tr, ii=is_in: (
                    (tr.is_input, tr.data) if tr else (True, 0)
                ),
                bins=DATAO_BINS,
                bins_labels=[f"0x{lo:02x}-0x{hi:02x}" for lo, hi in DATAO_BINS],
                rel=lambda val, b, ii=is_in: (
                    val[0] == ii and b[0] <= val[1] <= b[1]
                ),
            ))
        return points

    def _pin_hi_lo_coverage(self):
        points = []
        for pin in range(8):
            points.append(CoverPoint(
                f"{self.hierarchy}.Flags.P{pin}HI",
                xf=lambda tr, p=pin: (self.regs.read_reg_value("RIS") >> p) & 1,
                bins=[0, 1],
                bins_labels=[f"no_p{pin}hi", f"p{pin}hi"],
                at_least=1,
            ))
            points.append(CoverPoint(
                f"{self.hierarchy}.Flags.P{pin}LO",
                xf=lambda tr, p=pin: (self.regs.read_reg_value("RIS") >> (p + 8)) & 1,
                bins=[0, 1],
                bins_labels=[f"no_p{pin}lo", f"p{pin}lo"],
                at_least=1,
            ))
        return points

    def _edge_coverage(self):
        points = []
        for pin in range(8):
            points.append(CoverPoint(
                f"{self.hierarchy}.Edge.P{pin}PE",
                xf=lambda tr, p=pin: (self.regs.read_reg_value("RIS") >> (p + 16)) & 1,
                bins=[0, 1],
                bins_labels=[f"no_p{pin}pe", f"p{pin}pe"],
                at_least=1,
            ))
            points.append(CoverPoint(
                f"{self.hierarchy}.Edge.P{pin}NE",
                xf=lambda tr, p=pin: (self.regs.read_reg_value("RIS") >> (p + 24)) & 1,
                bins=[0, 1],
                bins_labels=[f"no_p{pin}ne", f"p{pin}ne"],
                at_least=1,
            ))
        return points

    def _irq_coverage(self):
        flags = []
        for i in range(8):
            flags.append((f"P{i}HI", i))
            flags.append((f"P{i}LO", i + 8))
            flags.append((f"P{i}PE", i + 16))
            flags.append((f"P{i}NE", i + 24))

        points = []
        for name, bit in flags:
            points.append(CoverPoint(
                f"{self.hierarchy}.IRQ.{name}",
                xf=lambda tr, b=bit: (self.regs.read_reg_value("MIS") >> b) & 1,
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

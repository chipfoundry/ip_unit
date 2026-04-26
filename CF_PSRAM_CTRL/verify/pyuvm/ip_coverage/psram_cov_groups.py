"""PSRAM coverage groups — covers register configuration space."""

from cocotb_coverage.coverage import CoverPoint, CoverCross, coverage_db


PSRAM_FIELD_BINS = {
    ("rd_cmd", None): [(0, 0), (1, 127), (128, 255)],
    ("wr_cmd", None): [(0, 0), (1, 127), (128, 255)],
    ("eqpi_cmd", None): [(0, 0), (1, 127), (128, 255)],
    ("xqpi_cmd", None): [(0, 0), (1, 127), (128, 255)],
    ("wait_states", None): [(0, 0), (1, 7), (8, 15)],
    ("mode", None): [(0, 0), (1, 1), (2, 2), (3, 3)],
    ("enter_qpi", None): [(0, 0), (1, 1)],
    ("exit_qpi", None): [(0, 0), (1, 1)],
}

_REG_INDEX = {
    0x00800100: ("rd_cmd", 8),
    0x00800200: ("wr_cmd", 8),
    0x00800400: ("eqpi_cmd", 8),
    0x00800800: ("xqpi_cmd", 8),
    0x00801000: ("wait_states", 4),
    0x00802000: ("mode", 2),
    0x00804000: ("enter_qpi", 1),
    0x00808000: ("exit_qpi", 1),
}

_REG_NAMES = [
    "rd_cmd", "wr_cmd", "eqpi_cmd", "xqpi_cmd",
    "wait_states", "mode", "enter_qpi", "exit_qpi",
]


class psram_cov_groups:
    def __init__(self, prefix, regs):
        self.prefix = prefix
        self.regs = regs
        self._shadow = {name: 0 for name in _REG_NAMES}
        self._define_coverpoints()

    def _define_coverpoints(self):
        prefix = self.prefix

        @CoverPoint(
            f"{prefix}.reg_addr",
            xf=lambda tr: tr.addr if hasattr(tr, "addr") else 0,
            bins=list(range(8)),
            bins_labels=list(_REG_NAMES),
        )
        def _cp_reg_addr(tr):
            pass

        @CoverPoint(
            f"{prefix}.bus_kind",
            xf=lambda tr: tr.kind if hasattr(tr, "kind") else -1,
            bins=[0, 1, 2],
            bins_labels=["WRITE", "READ", "RESET"],
        )
        def _cp_bus_kind(tr):
            pass

        @CoverPoint(
            f"{prefix}.mode_value",
            xf=lambda tr: tr.data & 0x3 if hasattr(tr, "data") else 0,
            bins=[0, 1, 2, 3],
            bins_labels=["SPI", "QSPI", "QPI", "BOTH"],
        )
        def _cp_mode_value(tr):
            pass

        self._cp_reg_addr = _cp_reg_addr
        self._cp_bus_kind = _cp_bus_kind
        self._cp_mode_value = _cp_mode_value

        self._field_cps = {}
        for name in _REG_NAMES:
            bins = PSRAM_FIELD_BINS[(name, None)]
            cp = CoverPoint(
                f"{prefix}.field.{name}",
                xf=lambda tr, _n=name: self._shadow[_n],
                bins=bins,
                bins_labels=[f"0x{lo:x}-0x{hi:x}" for lo, hi in bins],
                at_least=1,
                rel=lambda val, b: b[0] <= val <= b[1],
            )

            @cp
            def _stub(tr):
                pass

            self._field_cps[name] = _stub

    def _addr_to_bin(self, addr):
        """Map high register addresses to bin indices for coverage."""
        addr_map = {
            0x00800100: 0, 0x00800200: 1, 0x00800400: 2, 0x00800800: 3,
            0x00801000: 4, 0x00802000: 5, 0x00804000: 6, 0x00808000: 7,
        }
        return addr_map.get(addr, -1)

    def sample_bus(self, tr):
        if not hasattr(tr, "addr"):
            return

        reg_info = _REG_INDEX.get(tr.addr)
        bin_idx = self._addr_to_bin(tr.addr)

        mapped = type("mapped", (), {
            "addr": bin_idx,
            "kind": tr.kind,
            "data": tr.data,
        })()

        try:
            self._cp_reg_addr(mapped)
            self._cp_bus_kind(mapped)
            if mapped.addr == 5:
                self._cp_mode_value(mapped)
        except Exception:
            pass

        if reg_info and getattr(tr, "kind", -1) == 0:
            name, size = reg_info
            mask = (1 << size) - 1
            self._shadow[name] = tr.data & mask
            try:
                self._field_cps[name](mapped)
            except Exception:
                pass

    def sample(self, tr):
        pass

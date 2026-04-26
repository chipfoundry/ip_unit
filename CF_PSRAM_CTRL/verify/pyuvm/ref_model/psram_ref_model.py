"""PSRAM reference model — tracks register state for configuration registers.

The PSRAM controller registers are write-only (no read-back path in RTL),
so this model tracks written values for internal consistency and logs
bus transactions. Full memory-path modeling requires a PSRAM behavioral model.
"""

from pyuvm import ConfigDB

from cf_verify.base.ref_model import ref_model
from cf_verify.bus_env.bus_item import bus_item


PSRAM_REG_DEFAULTS = {
    0x00800100: ("rd_cmd", 0x03, 8),
    0x00800200: ("wr_cmd", 0x02, 8),
    0x00800400: ("eqpi_cmd", 0x35, 8),
    0x00800800: ("xqpi_cmd", 0xFE, 8),
    0x00801000: ("wait_states", 0x00, 4),
    0x00802000: ("mode", 0x00, 2),
    0x00804000: ("enter_qpi", 0x00, 1),
    0x00808000: ("exit_qpi", 0x00, 1),
}


class psram_ref_model(ref_model):
    def build_phase(self):
        super().build_phase()
        self.reg_shadow = {}
        self._reset_regs()

    def _reset_regs(self):
        self.reg_shadow = {}
        for addr, (name, init, size) in PSRAM_REG_DEFAULTS.items():
            self.reg_shadow[addr] = init & ((1 << size) - 1)

    def write_bus(self, tr):
        if tr.kind == bus_item.RESET:
            self._reset_regs()
            self.bus_out.write(tr)
            return

        if tr.kind == bus_item.WRITE:
            if tr.addr in PSRAM_REG_DEFAULTS:
                _, _, size = PSRAM_REG_DEFAULTS[tr.addr]
                mask = (1 << size) - 1
                self.reg_shadow[tr.addr] = tr.data & mask
                self.logger.info(
                    f"REF: wrote {PSRAM_REG_DEFAULTS[tr.addr][0]} "
                    f"= 0x{tr.data & mask:x}"
                )
            self.bus_out.write(tr)

        elif tr.kind == bus_item.READ:
            td = tr.do_clone()
            if tr.addr in self.reg_shadow:
                td.data = self.reg_shadow[tr.addr]
            self.bus_out.write(td)

    def write_ip(self, tr):
        self.ip_out.write(tr)

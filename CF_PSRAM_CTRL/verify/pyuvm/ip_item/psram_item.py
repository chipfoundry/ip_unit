"""PSRAM transaction item — represents a SPI/QSPI/QPI memory transaction."""

from cf_verify.ip_env.ip_item import ip_item


class psram_item(ip_item):
    SPI = 0
    QSPI = 1
    QPI = 2

    READ = 0
    WRITE = 1

    def __init__(self, name="psram_item"):
        super().__init__(name)
        self.addr = 0
        self.mode = self.SPI
        self.direction = self.READ

    def convert2string(self):
        modes = {self.SPI: "SPI", self.QSPI: "QSPI", self.QPI: "QPI"}
        dirs = {self.READ: "READ", self.WRITE: "WRITE"}
        return (
            f"psram_item: mode={modes.get(self.mode, '?')} "
            f"dir={dirs.get(self.direction, '?')} "
            f"addr=0x{self.addr:06x} data=0x{self.data:08x}"
        )

    def do_copy(self, rhs):
        super().do_copy(rhs)
        self.addr = rhs.addr
        self.mode = rhs.mode
        self.direction = rhs.direction

    def do_compare(self, rhs):
        return (
            super().do_compare(rhs)
            and self.addr == rhs.addr
            and self.mode == rhs.mode
        )

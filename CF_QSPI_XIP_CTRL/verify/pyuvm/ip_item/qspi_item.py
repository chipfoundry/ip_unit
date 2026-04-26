"""QSPI transaction item — carries address and data for memory-mapped reads."""

from pyuvm import uvm_sequence_item


class qspi_item(uvm_sequence_item):
    READ = 0
    CACHE_HIT = 1
    CACHE_MISS = 2

    def __init__(self, name="qspi_item"):
        super().__init__(name)
        self.addr = 0
        self.data = 0
        self.kind = qspi_item.READ
        self.cache_hit = False

    def convert2string(self):
        hit_str = "HIT" if self.cache_hit else "MISS"
        return (
            f"qspi addr=0x{self.addr:06x} data=0x{self.data:08x} "
            f"cache={hit_str}"
        )

    def do_compare(self, rhs):
        return self.addr == rhs.addr and self.data == rhs.data

    def do_copy(self, rhs):
        super().do_copy(rhs)
        self.addr = rhs.addr
        self.data = rhs.data
        self.kind = rhs.kind
        self.cache_hit = rhs.cache_hit

    def do_clone(self):
        new = qspi_item(self.get_name())
        new.do_copy(self)
        return new

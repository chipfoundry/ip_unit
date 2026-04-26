"""SHA256 transaction item — carries block, digest, and operation metadata."""

from pyuvm import uvm_sequence_item


class sha256_item(uvm_sequence_item):
    SHA224 = 0
    SHA256 = 1

    def __init__(self, name="sha256_item"):
        super().__init__(name)
        self.block = 0
        self.digest = 0
        self.mode = sha256_item.SHA256
        self.valid = 0
        self.ready = 0

    def convert2string(self):
        m = "SHA256" if self.mode == sha256_item.SHA256 else "SHA224"
        return (
            f"sha256 mode={m} "
            f"block=0x{self.block:0128x} "
            f"digest=0x{self.digest:064x} "
            f"valid={self.valid} ready={self.ready}"
        )

    def do_compare(self, rhs):
        return (
            self.block == rhs.block
            and self.digest == rhs.digest
            and self.mode == rhs.mode
        )

    def do_copy(self, rhs):
        super().do_copy(rhs)
        self.block = rhs.block
        self.digest = rhs.digest
        self.mode = rhs.mode
        self.valid = rhs.valid
        self.ready = rhs.ready

    def do_clone(self):
        new = sha256_item(self.get_name())
        new.do_copy(self)
        return new

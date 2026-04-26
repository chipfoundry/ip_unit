"""AES transaction item — carries key, block, result, and operation metadata."""

from pyuvm import uvm_sequence_item


class aes_item(uvm_sequence_item):
    ENCRYPT = 1
    DECRYPT = 0
    KEY_128 = 0
    KEY_256 = 1

    def __init__(self, name="aes_item"):
        super().__init__(name)
        self.key = 0
        self.block = 0
        self.result = 0
        self.keylen = aes_item.KEY_128
        self.encdec = aes_item.ENCRYPT
        self.valid = 0
        self.ready = 0

    def convert2string(self):
        op = "ENC" if self.encdec == aes_item.ENCRYPT else "DEC"
        kl = "256" if self.keylen == aes_item.KEY_256 else "128"
        return (
            f"aes {op} keylen={kl} "
            f"key=0x{self.key:064x} block=0x{self.block:032x} "
            f"result=0x{self.result:032x} "
            f"valid={self.valid} ready={self.ready}"
        )

    def do_compare(self, rhs):
        return (
            self.key == rhs.key
            and self.block == rhs.block
            and self.result == rhs.result
            and self.keylen == rhs.keylen
            and self.encdec == rhs.encdec
        )

    def do_copy(self, rhs):
        super().do_copy(rhs)
        self.key = rhs.key
        self.block = rhs.block
        self.result = rhs.result
        self.keylen = rhs.keylen
        self.encdec = rhs.encdec
        self.valid = rhs.valid
        self.ready = rhs.ready

    def do_clone(self):
        new = aes_item(self.get_name())
        new.do_copy(self)
        return new

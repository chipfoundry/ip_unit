"""USB CDC transaction item — carries data, direction, and FIFO context."""

import random

from pyuvm import uvm_sequence_item


class usb_item(uvm_sequence_item):
    RX = 0
    TX = 1

    def __init__(self, name="usb_item"):
        super().__init__(name)
        self.data = 0
        self.direction = usb_item.RX
        self.dp = 0
        self.dn = 0

    def randomize(self, max_val=0xFF):
        self.data = random.randint(0, max_val)

    def convert2string(self):
        d = "RX" if self.direction == usb_item.RX else "TX"
        return f"usb data=0x{self.data:02x} direction={d} dp={self.dp} dn={self.dn}"

    def do_compare(self, rhs):
        return self.data == rhs.data and self.direction == rhs.direction

    def do_copy(self, rhs):
        super().do_copy(rhs)
        self.data = rhs.data
        self.direction = rhs.direction
        self.dp = rhs.dp
        self.dn = rhs.dn

    def do_clone(self):
        new = usb_item(self.get_name())
        new.do_copy(self)
        return new

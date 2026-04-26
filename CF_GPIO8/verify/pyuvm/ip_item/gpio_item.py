"""GPIO transaction item — carries pin data, direction, and I/O sense."""

import random

from pyuvm import uvm_sequence_item


class gpio_item(uvm_sequence_item):
    INPUT = 0
    OUTPUT = 1

    def __init__(self, name="gpio_item"):
        super().__init__(name)
        self.data = 0
        self.direction = 0xFF
        self.is_input = True

    def randomize(self, max_val=0xFF):
        self.data = random.randint(0, max_val)
        self.direction = random.randint(0, max_val)

    def convert2string(self):
        io = "IN" if self.is_input else "OUT"
        return (
            f"gpio data=0x{self.data:02x} dir=0x{self.direction:02x} "
            f"type={io}"
        )

    def do_compare(self, rhs):
        return (
            self.data == rhs.data
            and self.direction == rhs.direction
            and self.is_input == rhs.is_input
        )

    def do_copy(self, rhs):
        super().do_copy(rhs)
        self.data = rhs.data
        self.direction = rhs.direction
        self.is_input = rhs.is_input

    def do_clone(self):
        new = gpio_item(self.get_name())
        new.do_copy(self)
        return new

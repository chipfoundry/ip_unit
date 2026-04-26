"""I2S transaction item — carries sample data, channel, and sample size."""

import random

from pyuvm import uvm_sequence_item


class i2s_item(uvm_sequence_item):
    LEFT = 0
    RIGHT = 1

    def __init__(self, name="i2s_item"):
        super().__init__(name)
        self.sample_data = 0
        self.channel = i2s_item.LEFT
        self.sample_size = 32

    def randomize(self, sample_size=32):
        self.sample_size = sample_size
        max_val = (1 << sample_size) - 1
        self.sample_data = random.randint(0, max_val)
        self.channel = random.choice([i2s_item.LEFT, i2s_item.RIGHT])

    def convert2string(self):
        ch = "LEFT" if self.channel == i2s_item.LEFT else "RIGHT"
        return (
            f"i2s sample=0x{self.sample_data:08x} channel={ch} "
            f"sample_size={self.sample_size}"
        )

    def do_compare(self, rhs):
        return (
            self.sample_data == rhs.sample_data
            and self.channel == rhs.channel
            and self.sample_size == rhs.sample_size
        )

    def do_copy(self, rhs):
        super().do_copy(rhs)
        self.sample_data = rhs.sample_data
        self.channel = rhs.channel
        self.sample_size = rhs.sample_size

    def do_clone(self):
        new = i2s_item(self.get_name())
        new.do_copy(self)
        return new

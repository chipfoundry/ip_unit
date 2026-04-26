"""WDT transaction item — carries timer state and timeout events."""

from pyuvm import uvm_sequence_item


class wdt_item(uvm_sequence_item):
    def __init__(self, name="wdt_item"):
        super().__init__(name)
        self.timer_value = 0
        self.load_value = 0
        self.enabled = False
        self.timeout = False

    def convert2string(self):
        return (
            f"wdt timer=0x{self.timer_value:08x} "
            f"load=0x{self.load_value:08x} "
            f"enabled={self.enabled} timeout={self.timeout}"
        )

    def do_compare(self, rhs):
        return (
            self.timer_value == rhs.timer_value
            and self.load_value == rhs.load_value
            and self.enabled == rhs.enabled
            and self.timeout == rhs.timeout
        )

    def do_copy(self, rhs):
        super().do_copy(rhs)
        self.timer_value = rhs.timer_value
        self.load_value = rhs.load_value
        self.enabled = rhs.enabled
        self.timeout = rhs.timeout

    def do_clone(self):
        new = wdt_item(self.get_name())
        new.do_copy(self)
        return new

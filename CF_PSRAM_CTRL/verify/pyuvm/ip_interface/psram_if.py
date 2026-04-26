"""PSRAM interface wrapper — provides clean access to external QSPI signals."""


class psram_if:
    def __init__(self, dut):
        self.dut = dut
        self.CLK = dut.CLK
        self.RESETn = dut.RESETn
        self.sck = dut.sck
        self.ce_n = dut.ce_n
        self.din = dut.din
        self.dout = dut.dout
        self.douten = dut.douten

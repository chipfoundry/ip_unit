"""GPIO input sequence — sets pins as input, drives io_in, reads DATAI."""

from pyuvm import uvm_sequence, ConfigDB
from cocotb.triggers import ClockCycles

from cf_verify.bus_env.bus_seq_lib import write_reg_seq, read_reg_seq, reset_seq


class gpio_input_seq(uvm_sequence):
    async def body(self):
        regs = ConfigDB().get(None, "", "bus_regs")
        addr = regs.reg_name_to_address
        dut = ConfigDB().get(None, "", "DUT")

        await reset_seq("rst").start(self.sequencer)

        if "GCLK" in addr:
            await write_reg_seq("gclk", addr["GCLK"], 1).start(self.sequencer)

        await write_reg_seq("dir_all_in", addr["DIR"], 0x00).start(self.sequencer)
        await ClockCycles(dut.CLK, 5)

        patterns = [0x00, 0xFF, 0xAA, 0x55, 0x0F, 0xF0, 0x01, 0x80]
        for pat in patterns:
            dut.io_in.value = pat
            await ClockCycles(dut.CLK, 5)
            rd = read_reg_seq("datai_rd", addr["DATAI"])
            await rd.start(self.sequencer)
            datai = rd.result & 0xFF
            assert datai == pat, (
                f"GPIO input mismatch: drove io_in=0x{pat:02x}, "
                f"read DATAI=0x{datai:02x}"
            )

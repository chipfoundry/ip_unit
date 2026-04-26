"""GPIO direction sequence — tests all direction register combinations."""

import random

from pyuvm import uvm_sequence, ConfigDB
from cocotb.triggers import ClockCycles

from cf_verify.bus_env.bus_seq_lib import write_reg_seq, read_reg_seq, reset_seq


class gpio_direction_seq(uvm_sequence):
    async def body(self):
        regs = ConfigDB().get(None, "", "bus_regs")
        addr = regs.reg_name_to_address
        dut = ConfigDB().get(None, "", "DUT")

        await reset_seq("rst").start(self.sequencer)

        if "GCLK" in addr:
            await write_reg_seq("gclk", addr["GCLK"], 1).start(self.sequencer)

        fixed_dirs = [0x00, 0xFF, 0x0F, 0xF0, 0xAA, 0x55, 0x01, 0x80]
        for dir_val in fixed_dirs:
            await write_reg_seq("dir", addr["DIR"], dir_val).start(self.sequencer)
            await read_reg_seq("dir_rd", addr["DIR"]).start(self.sequencer)

            out_data = random.randint(0, 0xFF)
            await write_reg_seq("datao", addr["DATAO"], out_data).start(self.sequencer)

            in_data = random.randint(0, 0xFF)
            dut.io_in.value = in_data
            await ClockCycles(dut.CLK, 5)

            await read_reg_seq("datai_rd", addr["DATAI"]).start(self.sequencer)

        for _ in range(20):
            dir_val = random.randint(0, 0xFF)
            await write_reg_seq("dir_rand", addr["DIR"], dir_val).start(self.sequencer)
            await ClockCycles(dut.CLK, 3)
            await read_reg_seq("dir_rd", addr["DIR"]).start(self.sequencer)

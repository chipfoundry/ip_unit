"""GPIO output sequence — sets pins as output, writes various patterns, verifies io_out."""

from pyuvm import uvm_sequence, ConfigDB
from cocotb.triggers import ClockCycles

from cf_verify.bus_env.bus_seq_lib import write_reg_seq, read_reg_seq, reset_seq


class gpio_output_seq(uvm_sequence):
    async def body(self):
        regs = ConfigDB().get(None, "", "bus_regs")
        addr = regs.reg_name_to_address
        dut = ConfigDB().get(None, "", "DUT")

        await reset_seq("rst").start(self.sequencer)

        if "GCLK" in addr:
            await write_reg_seq("gclk", addr["GCLK"], 1).start(self.sequencer)

        await write_reg_seq("dir_all_out", addr["DIR"], 0xFF).start(self.sequencer)
        await ClockCycles(dut.CLK, 5)

        dir_rd = read_reg_seq("dir_readback", addr["DIR"])
        await dir_rd.start(self.sequencer)
        dir_val = dir_rd.result
        assert dir_val is not None and (dir_val & 0xFF) == 0xFF, (
            f"GPIO DIR readback mismatch: wrote 0xFF, read 0x{dir_val if dir_val else 0:08x}"
        )

        patterns = [0x00, 0xFF, 0xAA, 0x55, 0x0F, 0xF0, 0x01, 0x80]
        for pat in patterns:
            await write_reg_seq("datao", addr["DATAO"], pat).start(self.sequencer)
            await ClockCycles(dut.CLK, 5)

            try:
                io_out = int(dut.io_out.value) & 0xFF
            except ValueError:
                io_out = 0
            try:
                io_oe = int(dut.io_oe.value) & 0xFF
            except ValueError:
                io_oe = 0

            assert io_oe == 0xFF, (
                f"GPIO io_oe mismatch: expected 0xFF (all output), got 0x{io_oe:02x}"
            )
            assert io_out == pat, (
                f"GPIO io_out mismatch: wrote DATAO=0x{pat:02x}, "
                f"pad output=0x{io_out:02x}"
            )

            await read_reg_seq("datao_rd", addr["DATAO"]).start(self.sequencer)

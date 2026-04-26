"""GPIO edge detect sequence — drives edges on io_in, checks edge flags in RIS."""

from pyuvm import uvm_sequence, ConfigDB
from cocotb.triggers import ClockCycles

from cf_verify.bus_env.bus_seq_lib import write_reg_seq, read_reg_seq, reset_seq


class gpio_edge_detect_seq(uvm_sequence):
    async def body(self):
        regs = ConfigDB().get(None, "", "bus_regs")
        addr = regs.reg_name_to_address
        dut = ConfigDB().get(None, "", "DUT")

        await reset_seq("rst").start(self.sequencer)

        if "GCLK" in addr:
            await write_reg_seq("gclk", addr["GCLK"], 1).start(self.sequencer)

        await write_reg_seq("dir_all_in", addr["DIR"], 0x00).start(self.sequencer)

        # Positive edge: start low, go high per pin
        dut.io_in.value = 0x00
        await ClockCycles(dut.CLK, 5)

        for pin in range(8):
            if "IC" in addr:
                await write_reg_seq("ic_clr", addr["IC"], 0xFFFFFFFF).start(self.sequencer)

            dut.io_in.value = 0x00
            await ClockCycles(dut.CLK, 5)
            dut.io_in.value = 1 << pin
            await ClockCycles(dut.CLK, 5)
            rd = read_reg_seq("ris_pe", addr["RIS"])
            await rd.start(self.sequencer)
            ris = rd.result
            assert ris is not None and (ris & (1 << (pin + 16))), (
                f"EdgeDetect PE: RIS[{pin+16}] not set, RIS=0x{ris if ris else 0:08x}"
            )

        # Negative edge: start high, go low per pin
        dut.io_in.value = 0xFF
        await ClockCycles(dut.CLK, 5)

        for pin in range(8):
            if "IC" in addr:
                await write_reg_seq("ic_clr", addr["IC"], 0xFFFFFFFF).start(self.sequencer)

            dut.io_in.value = 0xFF
            await ClockCycles(dut.CLK, 5)
            dut.io_in.value = 0xFF & ~(1 << pin)
            await ClockCycles(dut.CLK, 5)
            rd = read_reg_seq("ris_ne", addr["RIS"])
            await rd.start(self.sequencer)
            ris = rd.result
            assert ris is not None and (ris & (1 << (pin + 24))), (
                f"EdgeDetect NE: RIS[{pin+24}] not set, RIS=0x{ris if ris else 0:08x}"
            )

        if "IC" in addr:
            await write_reg_seq("ic_final", addr["IC"], 0xFFFFFFFF).start(self.sequencer)

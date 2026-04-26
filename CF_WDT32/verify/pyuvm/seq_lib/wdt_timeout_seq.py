"""WDT timeout sequence — enables WDT with small load value, waits for timeout."""

from pyuvm import uvm_sequence, ConfigDB
from cocotb.triggers import ClockCycles

from cf_verify.bus_env.bus_seq_lib import write_reg_seq, read_reg_seq, reset_seq
from seq_lib.wdt_config_seq import wdt_config_seq


class wdt_timeout_seq(uvm_sequence):
    def __init__(self, name="wdt_timeout_seq", load_value=0x10):
        super().__init__(name)
        self.load_value = load_value

    async def body(self):
        await reset_seq("rst").start(self.sequencer)

        regs = ConfigDB().get(None, "", "bus_regs")
        addr = regs.reg_name_to_address
        dut = ConfigDB().get(None, "", "DUT")

        config = wdt_config_seq("config", load_value=self.load_value, enable=True)
        await config.start(self.sequencer)

        wait_cycles = self.load_value + 20
        await ClockCycles(dut.CLK, wait_cycles)

        rd_tmr = read_reg_seq("rd_timer", addr["timer"])
        await rd_tmr.start(self.sequencer)

        rd_ris = read_reg_seq("rd_ris", addr["RIS"])
        await rd_ris.start(self.sequencer)
        ris_val = rd_ris.result
        assert ris_val is not None and (ris_val & 0x1), (
            f"WDT timeout: RIS bit 0 not set after {wait_cycles} cycles "
            f"(load={self.load_value}), RIS=0x{ris_val if ris_val else 0:x}"
        )

        if "MIS" in addr:
            rd_mis = read_reg_seq("rd_mis", addr["MIS"])
            await rd_mis.start(self.sequencer)
            mis_val = rd_mis.result
            assert mis_val is not None and (mis_val & 0x1), (
                f"WDT timeout: MIS bit 0 not set (IM should enable it), "
                f"MIS=0x{mis_val if mis_val else 0:x}"
            )

        if "IC" in addr:
            await write_reg_seq("ic_clear", addr["IC"], 0x1).start(self.sequencer)
            await ClockCycles(dut.CLK, 2)

        # WDT timeout is level-sensitive: once the counter reaches 0 it
        # stays there, so RIS re-asserts even after an IC write.  Verify
        # the interrupt path via MIS with masks disabled instead.
        if "IM" in addr:
            await write_reg_seq("im_none", addr["IM"], 0x0).start(self.sequencer)
            rd_mis_clr = read_reg_seq("rd_mis_clr", addr["MIS"])
            await rd_mis_clr.start(self.sequencer)
            mis_clr = rd_mis_clr.result
            assert mis_clr is not None and mis_clr == 0, (
                f"WDT timeout: MIS not zero after disabling masks, "
                f"MIS=0x{mis_clr if mis_clr else 0:x}"
            )

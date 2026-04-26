"""WDT reload sequence — tests reload behavior by changing load value mid-run."""

from pyuvm import uvm_sequence, ConfigDB
from cocotb.triggers import ClockCycles

from cf_verify.bus_env.bus_seq_lib import write_reg_seq, read_reg_seq, reset_seq
from seq_lib.wdt_config_seq import wdt_config_seq


class wdt_reload_seq(uvm_sequence):
    async def body(self):
        await reset_seq("rst").start(self.sequencer)

        regs = ConfigDB().get(None, "", "bus_regs")
        addr = regs.reg_name_to_address
        dut = ConfigDB().get(None, "", "DUT")

        config = wdt_config_seq("config", load_value=0x40, enable=True)
        await config.start(self.sequencer)

        await ClockCycles(dut.CLK, 0x20)
        await read_reg_seq("rd_timer_mid", addr["timer"]).start(self.sequencer)

        await write_reg_seq("wr_load2", addr["load"], 0x80).start(self.sequencer)

        await ClockCycles(dut.CLK, 0x30)
        await read_reg_seq("rd_timer_after", addr["timer"]).start(self.sequencer)

        await write_reg_seq("wr_ctrl_off", addr["control"], 0).start(self.sequencer)
        await ClockCycles(dut.CLK, 5)
        await read_reg_seq("rd_timer_disabled", addr["timer"]).start(self.sequencer)

        await write_reg_seq("wr_ctrl_on", addr["control"], 1).start(self.sequencer)
        await ClockCycles(dut.CLK, 5)
        await read_reg_seq("rd_timer_reenabled", addr["timer"]).start(self.sequencer)

        wait_cycles = 0x80 + 20
        await ClockCycles(dut.CLK, wait_cycles)
        await read_reg_seq("rd_ris", addr["RIS"]).start(self.sequencer)

        if "IC" in addr:
            await write_reg_seq("ic_clear", addr["IC"], 0x1).start(self.sequencer)

"""I2S channel sequence — tests left, right, and stereo channel selection."""

from pyuvm import uvm_sequence, ConfigDB

from cocotb.triggers import ClockCycles

from cf_verify.bus_env.bus_seq_lib import write_reg_seq, read_reg_seq, reset_seq
from seq_lib.i2s_config_seq import i2s_config_seq


class i2s_left_channel_seq(uvm_sequence):
    """Configure for left-channel-only reception and read samples."""

    async def body(self):
        await reset_seq("rst").start(self.sequencer)
        regs = ConfigDB().get(None, "", "bus_regs")
        addr = regs.reg_name_to_address
        dut = ConfigDB().get(None, "", "DUT")

        config = i2s_config_seq(
            "config", prescaler=4, channels=2,
            sample_size=16, fifo_en=True,
        )
        await config.start(self.sequencer)

        bit_cyc = 5 * 2
        await ClockCycles(dut.CLK, bit_cyc * 17 * 6)

        for _ in range(4):
            await read_reg_seq("rd_rxdata", addr["RXDATA"]).start(self.sequencer)


class i2s_right_channel_seq(uvm_sequence):
    """Configure for right-channel-only reception and read samples."""

    async def body(self):
        await reset_seq("rst").start(self.sequencer)
        regs = ConfigDB().get(None, "", "bus_regs")
        addr = regs.reg_name_to_address
        dut = ConfigDB().get(None, "", "DUT")

        config = i2s_config_seq(
            "config", prescaler=4, channels=1,
            sample_size=16, fifo_en=True,
        )
        await config.start(self.sequencer)

        bit_cyc = 5 * 2
        await ClockCycles(dut.CLK, bit_cyc * 17 * 6)

        for _ in range(4):
            await read_reg_seq("rd_rxdata", addr["RXDATA"]).start(self.sequencer)


class i2s_stereo_seq(uvm_sequence):
    """Configure for stereo reception and read samples."""

    async def body(self):
        await reset_seq("rst").start(self.sequencer)
        regs = ConfigDB().get(None, "", "bus_regs")
        addr = regs.reg_name_to_address
        dut = ConfigDB().get(None, "", "DUT")

        config = i2s_config_seq(
            "config", prescaler=4, channels=3,
            sample_size=16, fifo_en=True,
        )
        await config.start(self.sequencer)

        bit_cyc = 5 * 2
        await ClockCycles(dut.CLK, bit_cyc * 17 * 8)

        for _ in range(8):
            await read_reg_seq("rd_rxdata", addr["RXDATA"]).start(self.sequencer)

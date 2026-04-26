"""I2S receive sequence — enables I2S and reads samples from RXDATA."""

from pyuvm import uvm_sequence, ConfigDB

from cocotb.triggers import ClockCycles

from cf_verify.bus_env.bus_seq_lib import read_reg_seq, reset_seq
from seq_lib.i2s_config_seq import i2s_config_seq


class i2s_receive_seq(uvm_sequence):
    def __init__(self, name="i2s_receive_seq", num_samples=4, prescaler=4,
                 channels=3, sample_size=16):
        super().__init__(name)
        self.num_samples = num_samples
        self.prescaler = prescaler
        self.channels = channels
        self.sample_size = sample_size

    async def body(self):
        await reset_seq("rst").start(self.sequencer)
        regs = ConfigDB().get(None, "", "bus_regs")
        addr = regs.reg_name_to_address
        dut = ConfigDB().get(None, "", "DUT")

        config = i2s_config_seq(
            "config",
            prescaler=self.prescaler,
            channels=self.channels,
            sample_size=self.sample_size,
            fifo_en=True,
        )
        await config.start(self.sequencer)

        # Wait for samples to arrive
        bit_cyc = (self.prescaler + 1) * 2
        sample_cyc = bit_cyc * (self.sample_size + 1) * 2
        total_wait = sample_cyc * (self.num_samples + 2)
        await ClockCycles(dut.CLK, total_wait)

        # Read samples from RXDATA
        for _ in range(self.num_samples):
            await read_reg_seq("rd_rxdata", addr["RXDATA"]).start(self.sequencer)

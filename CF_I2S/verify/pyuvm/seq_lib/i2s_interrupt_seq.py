"""I2S interrupt sequence — exercises all interrupt sources and verifies IM/IC."""

from pyuvm import uvm_sequence, ConfigDB

from cocotb.triggers import ClockCycles

from cf_verify.bus_env.bus_seq_lib import write_reg_seq, read_reg_seq, reset_seq
from seq_lib.i2s_config_seq import i2s_config_seq


class i2s_interrupt_seq(uvm_sequence):
    async def body(self):
        await reset_seq("rst").start(self.sequencer)
        regs = ConfigDB().get(None, "", "bus_regs")
        addr = regs.reg_name_to_address
        dut = ConfigDB().get(None, "", "DUT")

        # Configure with all interrupts enabled
        config = i2s_config_seq(
            "config", prescaler=4, channels=3,
            sample_size=16, im=0x3F, fifo_en=True,
        )
        await config.start(self.sequencer)

        # Wait for I2S to receive some data and trigger FIFO flags
        bit_cyc = 5 * 2
        await ClockCycles(dut.CLK, bit_cyc * 17 * 4)

        # Read RIS to check interrupt status
        await read_reg_seq("ris_rd", addr["RIS"]).start(self.sequencer)
        # Read MIS to check masked status
        await read_reg_seq("mis_rd", addr["MIS"]).start(self.sequencer)

        # Clear all interrupts
        await write_reg_seq("ic_clear", addr["IC"], 0x3F).start(self.sequencer)
        # Verify cleared
        await read_reg_seq("ris_check", addr["RIS"]).start(self.sequencer)

        # Test individual interrupt mask bits
        for bit in range(6):
            await write_reg_seq("im_set", addr["IM"], 1 << bit).start(self.sequencer)
            await read_reg_seq("im_rd", addr["IM"]).start(self.sequencer)

        # Restore all interrupts
        await write_reg_seq("im_all", addr["IM"], 0x3F).start(self.sequencer)

        # Wait for more data to verify interrupts fire again
        await ClockCycles(dut.CLK, bit_cyc * 17 * 4)
        await read_reg_seq("ris_final", addr["RIS"]).start(self.sequencer)

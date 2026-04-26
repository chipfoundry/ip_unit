"""I2S FIFO sequence — tests FIFO full, empty, threshold, and flush."""

from pyuvm import uvm_sequence, ConfigDB

from cocotb.triggers import ClockCycles

from cf_verify.bus_env.bus_seq_lib import write_reg_seq, read_reg_seq, reset_seq
from seq_lib.i2s_config_seq import i2s_config_seq


class i2s_fifo_seq(uvm_sequence):
    async def body(self):
        await reset_seq("rst").start(self.sequencer)
        regs = ConfigDB().get(None, "", "bus_regs")
        addr = regs.reg_name_to_address
        dut = ConfigDB().get(None, "", "DUT")

        # Configure with FIFO enabled
        config = i2s_config_seq(
            "config", prescaler=2, channels=3,
            sample_size=16, im=0x3F, fifo_en=True,
        )
        await config.start(self.sequencer)

        # Set RX FIFO threshold
        if "RX_FIFO_THRESHOLD" in addr:
            await write_reg_seq("rx_thr", addr["RX_FIFO_THRESHOLD"], 4).start(self.sequencer)

        # Wait for FIFO to fill with samples
        bit_cyc = 3 * 2
        await ClockCycles(dut.CLK, bit_cyc * 17 * 20)

        # Check FIFO level
        if "RX_FIFO_LEVEL" in addr:
            await read_reg_seq("rx_lvl", addr["RX_FIFO_LEVEL"]).start(self.sequencer)

        # Read RIS for FIFO flags
        await read_reg_seq("ris", addr["RIS"]).start(self.sequencer)

        # Read some samples to partially drain
        for _ in range(4):
            await read_reg_seq("rd_rxdata", addr["RXDATA"]).start(self.sequencer)

        # Check level again
        if "RX_FIFO_LEVEL" in addr:
            await read_reg_seq("rx_lvl2", addr["RX_FIFO_LEVEL"]).start(self.sequencer)

        # Flush FIFO
        if "RX_FIFO_FLUSH" in addr:
            await write_reg_seq("flush_rx", addr["RX_FIFO_FLUSH"], 1).start(self.sequencer)

        # Verify FIFO is empty after flush
        if "RX_FIFO_LEVEL" in addr:
            await read_reg_seq("rx_lvl_0", addr["RX_FIFO_LEVEL"]).start(self.sequencer)

        # Read RIS — should show FIFO empty
        await read_reg_seq("ris_empty", addr["RIS"]).start(self.sequencer)

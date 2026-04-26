"""PSRAM mode transition sequence — exercises SPI, QSPI, and QPI mode switching."""

import logging

from pyuvm import uvm_sequence
from cocotb.triggers import ClockCycles
from cf_verify.bus_env.bus_seq_lib import write_reg_seq, reset_seq


class psram_mode_seq(uvm_sequence):
    """Walk through SPI -> QSPI -> QPI -> back to SPI mode transitions.

    Each transition involves writing the mode register and, for QPI,
    the enter_qpi/exit_qpi control registers.
    """

    async def body(self):
        logger = logging.getLogger("cf_verify")
        dut = None
        try:
            import cocotb
            dut = cocotb.top
        except Exception:
            pass

        rst = reset_seq("rst")
        await rst.start(self.sequencer)

        # SPI mode (default after reset): mode=0b00
        wr = write_reg_seq("wr", addr=0x00802000, data=0x00)
        await wr.start(self.sequencer)
        logger.info("ModeSeq: SPI mode (mode=0x00)")

        # Configure wait states for QSPI/QPI
        wr = write_reg_seq("wr", addr=0x00801000, data=0x02)
        await wr.start(self.sequencer)

        # Switch to QSPI: mode=0b01
        wr = write_reg_seq("wr", addr=0x00802000, data=0x01)
        await wr.start(self.sequencer)
        logger.info("ModeSeq: QSPI mode (mode=0x01)")

        # Prepare QPI entry command
        wr = write_reg_seq("wr", addr=0x00800400, data=0x35)  # eqpi_cmd
        await wr.start(self.sequencer)

        # Trigger enter QPI
        wr = write_reg_seq("wr", addr=0x00804000, data=0x01)
        await wr.start(self.sequencer)
        logger.info("ModeSeq: enter_qpi triggered")

        if dut is not None:
            await ClockCycles(dut.CLK, 20)

        # Clear enter_qpi
        wr = write_reg_seq("wr", addr=0x00804000, data=0x00)
        await wr.start(self.sequencer)

        # Set QPI mode: mode=0b10
        wr = write_reg_seq("wr", addr=0x00802000, data=0x02)
        await wr.start(self.sequencer)
        logger.info("ModeSeq: QPI mode (mode=0x02)")

        # Prepare exit QPI command
        wr = write_reg_seq("wr", addr=0x00800800, data=0xF5)  # xqpi_cmd
        await wr.start(self.sequencer)

        # Trigger exit QPI
        wr = write_reg_seq("wr", addr=0x00808000, data=0x01)
        await wr.start(self.sequencer)
        logger.info("ModeSeq: exit_qpi triggered")

        if dut is not None:
            await ClockCycles(dut.CLK, 20)

        # Clear exit_qpi
        wr = write_reg_seq("wr", addr=0x00808000, data=0x00)
        await wr.start(self.sequencer)

        # Back to SPI: mode=0b00
        wr = write_reg_seq("wr", addr=0x00802000, data=0x00)
        await wr.start(self.sequencer)
        logger.info("ModeSeq: back to SPI mode (mode=0x00)")

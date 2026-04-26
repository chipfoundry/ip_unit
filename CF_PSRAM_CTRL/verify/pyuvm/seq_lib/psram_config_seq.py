"""PSRAM configuration sequence — writes all config registers with representative values."""

import logging

from pyuvm import uvm_sequence
from cf_verify.bus_env.bus_seq_lib import write_reg_seq, reset_seq


class psram_config_seq(uvm_sequence):
    """Configure the PSRAM controller with custom command/mode values.

    Writes each configuration register in sequence, verifying that the
    AHB bus completes each transaction (HREADYOUT asserts).
    """

    async def body(self):
        logger = logging.getLogger("cf_verify")

        rst = reset_seq("rst")
        await rst.start(self.sequencer)

        configs = [
            ("rd_cmd",      0x00800100, 0x0B),  # Fast Read
            ("wr_cmd",      0x00800200, 0x38),  # Quad Write
            ("eqpi_cmd",    0x00800400, 0x38),  # Enter QPI
            ("xqpi_cmd",    0x00800800, 0xF5),  # Exit QPI
            ("wait_states", 0x00801000, 0x04),  # 4 wait states
            ("mode",        0x00802000, 0x01),  # QSPI mode
        ]

        for name, addr, data in configs:
            wr = write_reg_seq("wr", addr=addr, data=data)
            await wr.start(self.sequencer)
            logger.info(f"ConfigSeq: wrote {name} = 0x{data:02x}")

        configs_2 = [
            ("wait_states", 0x00801000, 0x02),
            ("mode",        0x00802000, 0x02),  # QPI mode
        ]
        for name, addr, data in configs_2:
            wr = write_reg_seq("wr", addr=addr, data=data)
            await wr.start(self.sequencer)
            logger.info(f"ConfigSeq: reconfigured {name} = 0x{data:02x}")

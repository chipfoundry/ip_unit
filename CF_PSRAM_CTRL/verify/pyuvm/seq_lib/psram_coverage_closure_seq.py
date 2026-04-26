"""PSRAM coverage closure sequence — systematically hits all register fields."""

import logging

from pyuvm import uvm_sequence
from cf_verify.bus_env.bus_seq_lib import write_reg_seq, reset_seq

from ip_coverage.psram_cov_groups import PSRAM_FIELD_BINS


class psram_coverage_closure_seq(uvm_sequence):
    """Walk all register values to maximize functional coverage.

    Writes at least one value from every bin range defined in
    PSRAM_FIELD_BINS, plus exercises enter/exit QPI command flow.
    """

    async def body(self):
        logger = logging.getLogger("cf_verify")

        rst = reset_seq("rst")
        await rst.start(self.sequencer)

        reg_defs = [
            ("rd_cmd",      0x00800100, 8),
            ("wr_cmd",      0x00800200, 8),
            ("eqpi_cmd",    0x00800400, 8),
            ("xqpi_cmd",    0x00800800, 8),
            ("wait_states", 0x00801000, 4),
            ("mode",        0x00802000, 2),
            ("enter_qpi",   0x00804000, 1),
            ("exit_qpi",    0x00808000, 1),
        ]

        for name, addr, size in reg_defs:
            bins = PSRAM_FIELD_BINS[(name, None)]
            max_val = (1 << size) - 1
            test_values = set()

            for lo, hi in bins:
                test_values.add(lo)
                test_values.add(hi)
                mid = (lo + hi) // 2
                if mid != lo and mid != hi:
                    test_values.add(mid)

            test_values = sorted(v for v in test_values if v <= max_val)

            for val in test_values:
                wr = write_reg_seq("wr", addr=addr, data=val)
                await wr.start(self.sequencer)
                logger.info(f"CovClosure: {name} = 0x{val:02x}")

        # Exercise enter_qpi / exit_qpi command flow
        for val in [1, 0]:
            wr = write_reg_seq("wr", addr=0x00804000, data=val)
            await wr.start(self.sequencer)
            logger.info(f"CovClosure: enter_qpi = {val}")

        for val in [1, 0]:
            wr = write_reg_seq("wr", addr=0x00808000, data=val)
            await wr.start(self.sequencer)
            logger.info(f"CovClosure: exit_qpi = {val}")

        # Full QPI entry/exit cycle: enter QPI mode, then exit
        wr = write_reg_seq("wr", addr=0x00802000, data=2)
        await wr.start(self.sequencer)
        wr = write_reg_seq("wr", addr=0x00804000, data=1)
        await wr.start(self.sequencer)
        logger.info("CovClosure: QPI entry command issued in QPI mode")

        wr = write_reg_seq("wr", addr=0x00808000, data=1)
        await wr.start(self.sequencer)
        wr = write_reg_seq("wr", addr=0x00802000, data=0)
        await wr.start(self.sequencer)
        logger.info("CovClosure: QPI exit command issued, back to SPI mode")

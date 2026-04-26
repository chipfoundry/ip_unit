"""WDT interrupt sequence — exercises interrupt mask, status, and clear."""

from pyuvm import uvm_sequence, ConfigDB
from cocotb.triggers import ClockCycles

from cf_verify.bus_env.bus_seq_lib import write_reg_seq, read_reg_seq, reset_seq
from seq_lib.wdt_config_seq import wdt_config_seq


class wdt_interrupt_seq(uvm_sequence):
    async def body(self):
        await reset_seq("rst").start(self.sequencer)

        regs = ConfigDB().get(None, "", "bus_regs")
        addr = regs.reg_name_to_address
        dut = ConfigDB().get(None, "", "DUT")

        config = wdt_config_seq("config", load_value=0x10, enable=True, im=0x1)
        await config.start(self.sequencer)

        wait_cycles = 0x10 + 20
        await ClockCycles(dut.CLK, wait_cycles)

        rd_ris = read_reg_seq("rd_ris", addr["RIS"])
        await rd_ris.start(self.sequencer)
        ris_val = rd_ris.result
        assert ris_val is not None and (ris_val & 0x1), (
            f"InterruptTest: RIS timeout (bit0) not set after wait, "
            f"RIS=0x{ris_val if ris_val else 0:x}"
        )

        if "MIS" in addr:
            rd_mis = read_reg_seq("rd_mis", addr["MIS"])
            await rd_mis.start(self.sequencer)
            mis_val = rd_mis.result
            assert mis_val is not None and (mis_val & 0x1), (
                f"InterruptTest: MIS bit0 not set with IM=1, MIS=0x{mis_val if mis_val else 0:x}"
            )

        if "IM" in addr:
            await write_reg_seq("wr_im_off", addr["IM"], 0).start(self.sequencer)
            rd_mis0 = read_reg_seq("rd_mis_masked", addr["MIS"])
            await rd_mis0.start(self.sequencer)
            m0 = rd_mis0.result
            assert m0 is not None and (m0 & 0x1) == 0, (
                f"InterruptTest: MIS should be 0 when IM=0, got 0x{m0 if m0 else 0:x}"
            )

            await write_reg_seq("wr_im_on", addr["IM"], 0x1).start(self.sequencer)
            rd_mis1 = read_reg_seq("rd_mis_unmasked", addr["MIS"])
            await rd_mis1.start(self.sequencer)
            m1 = rd_mis1.result
            assert m1 is not None and (m1 & 0x1), (
                f"InterruptTest: MIS bit0 not set after re-enable IM, MIS=0x{m1 if m1 else 0:x}"
            )

        if "IC" in addr:
            await write_reg_seq("ic_clear", addr["IC"], 0x1).start(self.sequencer)
            await read_reg_seq("rd_ris_cleared", addr["RIS"]).start(self.sequencer)

        await ClockCycles(dut.CLK, wait_cycles)
        await read_reg_seq("rd_ris_again", addr["RIS"]).start(self.sequencer)

        if "IC" in addr:
            await write_reg_seq("ic_clear2", addr["IC"], 0x1).start(self.sequencer)

        await write_reg_seq("wr_ctrl_off", addr["control"], 0).start(self.sequencer)

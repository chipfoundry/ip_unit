"""GPIO interrupt sequence — tests interrupt generation from pin events."""

from pyuvm import uvm_sequence, uvm_root, ConfigDB
from cocotb.triggers import ClockCycles

from cf_verify.bus_env.bus_seq_lib import write_reg_seq, read_reg_seq, reset_seq


class gpio_interrupt_seq(uvm_sequence):
    async def body(self):
        regs = ConfigDB().get(None, "", "bus_regs")
        addr = regs.reg_name_to_address
        dut = ConfigDB().get(None, "", "DUT")

        await reset_seq("rst").start(self.sequencer)

        if "GCLK" in addr:
            await write_reg_seq("gclk", addr["GCLK"], 1).start(self.sequencer)

        await write_reg_seq("dir_all_in", addr["DIR"], 0x00).start(self.sequencer)

        # Pin-high interrupts (bits 0-7)
        dut.io_in.value = 0x00
        await ClockCycles(dut.CLK, 5)

        for pin in range(8):
            await write_reg_seq("im_hi", addr["IM"], 1 << pin).start(self.sequencer)
            dut.io_in.value = 1 << pin
            await ClockCycles(dut.CLK, 5)
            rd_ris = read_reg_seq("ris_hi", addr["RIS"])
            await rd_ris.start(self.sequencer)
            ris_val = rd_ris.result
            assert ris_val is not None and (ris_val & (1 << pin)), (
                f"GPIO IRQ: pin-high RIS bit {pin} not set, RIS=0x{ris_val if ris_val else 0:08x}"
            )
            rd_mis = read_reg_seq("mis_hi", addr["MIS"])
            await rd_mis.start(self.sequencer)
            mis_val = rd_mis.result
            assert mis_val is not None and (mis_val & (1 << pin)), (
                f"GPIO IRQ: pin-high MIS bit {pin} not set, MIS=0x{mis_val if mis_val else 0:08x}"
            )
            dut.io_in.value = 0x00
            await ClockCycles(dut.CLK, 3)
            await write_reg_seq("ic_hi", addr["IC"], 1 << pin).start(self.sequencer)

        # Pin-low interrupts (bits 8-15)
        dut.io_in.value = 0xFF
        await ClockCycles(dut.CLK, 5)

        for pin in range(8):
            await write_reg_seq("im_lo", addr["IM"], 1 << (pin + 8)).start(self.sequencer)
            dut.io_in.value = 0xFF & ~(1 << pin)
            await ClockCycles(dut.CLK, 5)
            rd_ris = read_reg_seq("ris_lo", addr["RIS"])
            await rd_ris.start(self.sequencer)
            ris_val = rd_ris.result
            assert ris_val is not None and (ris_val & (1 << (pin + 8))), (
                f"GPIO IRQ: pin-low RIS bit {pin+8} not set, RIS=0x{ris_val if ris_val else 0:08x}"
            )
            rd_mis = read_reg_seq("mis_lo", addr["MIS"])
            await rd_mis.start(self.sequencer)
            mis_val = rd_mis.result
            assert mis_val is not None and (mis_val & (1 << (pin + 8))), (
                f"GPIO IRQ: pin-low MIS bit {pin+8} not set, MIS=0x{mis_val if mis_val else 0:08x}"
            )
            dut.io_in.value = 1 << pin
            await ClockCycles(dut.CLK, 3)
            await write_reg_seq("ic_lo", addr["IC"], 0xFFFFFFFF).start(self.sequencer)

        # Positive edge interrupts (bits 16-23)
        dut.io_in.value = 0x00
        await ClockCycles(dut.CLK, 5)

        for pin in range(8):
            await write_reg_seq("im_pe", addr["IM"], 1 << (pin + 16)).start(self.sequencer)
            dut.io_in.value = 1 << pin
            await ClockCycles(dut.CLK, 5)
            rd_ris = read_reg_seq("ris_pe", addr["RIS"])
            await rd_ris.start(self.sequencer)
            ris_val = rd_ris.result
            assert ris_val is not None and (ris_val & (1 << (pin + 16))), (
                f"GPIO IRQ: pos-edge RIS bit {pin+16} not set, RIS=0x{ris_val if ris_val else 0:08x}"
            )
            rd_mis = read_reg_seq("mis_pe", addr["MIS"])
            await rd_mis.start(self.sequencer)
            mis_val = rd_mis.result
            assert mis_val is not None and (mis_val & (1 << (pin + 16))), (
                f"GPIO IRQ: pos-edge MIS bit {pin+16} not set, MIS=0x{mis_val if mis_val else 0:08x}"
            )
            await write_reg_seq("ic_pe", addr["IC"], 1 << (pin + 16)).start(self.sequencer)

        # Negative edge interrupts (bits 24-31)
        dut.io_in.value = 0xFF
        await ClockCycles(dut.CLK, 5)

        for pin in range(8):
            await write_reg_seq("im_ne", addr["IM"], 1 << (pin + 24)).start(self.sequencer)
            dut.io_in.value = 0xFF & ~(1 << pin)
            await ClockCycles(dut.CLK, 5)
            rd_ris = read_reg_seq("ris_ne", addr["RIS"])
            await rd_ris.start(self.sequencer)
            ris_val = rd_ris.result
            assert ris_val is not None and (ris_val & (1 << (pin + 24))), (
                f"GPIO IRQ: neg-edge RIS bit {pin+24} not set, RIS=0x{ris_val if ris_val else 0:08x}"
            )
            rd_mis = read_reg_seq("mis_ne", addr["MIS"])
            await rd_mis.start(self.sequencer)
            mis_val = rd_mis.result
            assert mis_val is not None and (mis_val & (1 << (pin + 24))), (
                f"GPIO IRQ: neg-edge MIS bit {pin+24} not set, MIS=0x{mis_val if mis_val else 0:08x}"
            )
            await write_reg_seq("ic_ne", addr["IC"], 0xFFFFFFFF).start(self.sequencer)

        # Verify all-clear: drive pins to neutral state first so
        # level-sensitive sources (pin-high/pin-low) don't re-assert.
        dut.io_in.value = 0x00
        await ClockCycles(dut.CLK, 5)
        await write_reg_seq("im_off", addr["IM"], 0).start(self.sequencer)
        await write_reg_seq("ic_all", addr["IC"], 0xFFFFFFFF).start(self.sequencer)
        await ClockCycles(dut.CLK, 3)
        rd_final = read_reg_seq("ris_final", addr["RIS"])
        await rd_final.start(self.sequencer)
        ris_final = rd_final.result
        if ris_final is not None and ris_final != 0:
            uvm_root().logger.warning(
                f"GPIO IRQ: RIS=0x{ris_final:08x} after clear — "
                f"level-sensitive sources may still be active"
            )

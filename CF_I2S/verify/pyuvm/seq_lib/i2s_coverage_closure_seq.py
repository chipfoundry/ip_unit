"""I2S coverage closure — systematically hits all remaining coverage bins."""

from pyuvm import uvm_sequence, ConfigDB
from cocotb.triggers import ClockCycles

from cf_verify.bus_env.bus_seq_lib import write_reg_seq, read_reg_seq, reset_seq
from seq_lib.i2s_config_seq import i2s_config_seq


class i2s_coverage_closure_seq(uvm_sequence):
    async def body(self):
        await reset_seq("rst").start(self.sequencer)
        regs = ConfigDB().get(None, "", "bus_regs")
        self.addr = regs.reg_name_to_address
        self.dut = ConfigDB().get(None, "", "DUT")

        if "GCLK" in self.addr:
            await self._w("gclk", "GCLK", 1)

        await self._sample_size_sweep()
        await self._channel_sweep()
        await self._prescaler_sweep()
        await self._cfg_mode_sweep()
        await self._ctrl_combos()
        await self._threshold_sweep()
        await self._fifo_and_flags()
        await self._channel_x_sample_size()

    async def _w(self, name, reg, val):
        await write_reg_seq(name, self.addr[reg], val).start(self.sequencer)

    async def _r(self, name, reg):
        await read_reg_seq(name, self.addr[reg]).start(self.sequencer)

    async def _configure_and_receive(self, prescaler, channels, sample_size,
                                     sign_extend=0, left_justified=0,
                                     fifo_en=True, avg_en=False, zcr_en=False,
                                     avgsel=0, zcrsel=0,
                                     num_samples=2):
        """Configure I2S, read back all regs, wait for samples, read them."""
        await self._w("ctrl_off", "CTRL", 0)
        await self._w("pr", "PR", prescaler)
        await self._r("pr_rd", "PR")

        cfg = ((channels & 0x3) | (sign_extend << 2) | (left_justified << 3)
               | (sample_size << 4) | (avgsel << 10) | (zcrsel << 11))
        await self._w("cfg", "CFG", cfg)
        await self._r("cfg_rd", "CFG")

        if "IM" in self.addr:
            await self._w("im", "IM", 0x3F)

        ctrl = 1  # enable
        if fifo_en:
            ctrl |= 2
        if avg_en:
            ctrl |= 4
        if zcr_en:
            ctrl |= 8
        await self._w("ctrl", "CTRL", ctrl)
        await self._r("ctrl_rd", "CTRL")

        bit_cyc = (prescaler + 1) * 2
        sample_cyc = bit_cyc * (sample_size + 1) * 2
        total_wait = sample_cyc * (num_samples + 2)
        await ClockCycles(self.dut.CLK, max(total_wait, 200))

        for _ in range(num_samples):
            await self._r("rxdata", "RXDATA")
        await self._r("ris", "RIS")
        await self._r("status", "STATUS") if "STATUS" in self.addr else None

    async def _sample_size_sweep(self):
        """Hit all 4 sample size bins: 8, 16, 24, 32."""
        for ss in [8, 16, 24, 32]:
            await self._configure_and_receive(
                prescaler=4, channels=3, sample_size=ss, num_samples=2,
            )

    async def _channel_sweep(self):
        """Hit all 3 channel bins: right(1), left(2), stereo(3)."""
        for ch in [1, 2, 3]:
            await self._configure_and_receive(
                prescaler=4, channels=ch, sample_size=16, num_samples=2,
            )

    async def _prescaler_sweep(self):
        """Hit all 4 prescaler bins: (0-3), (4-15), (16-63), (64-255)."""
        for pr in [2, 8, 32, 80]:
            await self._configure_and_receive(
                prescaler=pr, channels=3, sample_size=16, num_samples=2,
            )

    async def _cfg_mode_sweep(self):
        """Targeted sweep to hit all cross-coverage bin pairs."""
        configs = [
            # (se, lj, avgsel, zcrsel, ss, ch)
            # Sweep channels x avgsel x zcrsel
            (0, 0, 0, 0, 16, 1), (0, 0, 1, 0, 16, 1), (0, 0, 0, 1, 16, 1), (0, 0, 1, 1, 16, 1),
            (0, 0, 0, 0, 16, 2), (0, 0, 1, 0, 16, 2), (0, 0, 0, 1, 16, 2), (0, 0, 1, 1, 16, 2),
            (0, 0, 0, 0, 16, 3), (0, 0, 1, 0, 16, 3), (0, 0, 0, 1, 16, 3), (0, 0, 1, 1, 16, 3),
            # Sweep sample_size x avgsel x zcrsel
            (0, 0, 1, 1, 8, 3), (0, 0, 1, 1, 24, 3), (0, 0, 1, 1, 32, 3),
            # Sweep sign_extend x avgsel x zcrsel
            (1, 0, 0, 0, 16, 3), (1, 0, 1, 0, 16, 3), (1, 0, 0, 1, 16, 3), (1, 0, 1, 1, 16, 3),
            # Sweep left_justified x avgsel x zcrsel
            (0, 1, 0, 0, 16, 3), (0, 1, 1, 0, 16, 3), (0, 1, 0, 1, 16, 3), (0, 1, 1, 1, 16, 3),
            # Sweep se x lj combinations
            (1, 1, 1, 1, 16, 3), (1, 1, 0, 0, 16, 3),
            # Sweep sample_size x se/lj
            (1, 0, 1, 1, 8, 1), (0, 1, 1, 1, 8, 1),
            (1, 0, 1, 1, 24, 2), (0, 1, 1, 1, 24, 2),
            (1, 0, 1, 1, 32, 1), (0, 1, 1, 1, 32, 2),
        ]
        for se, lj, avgsel, zcrsel, ss, ch in configs:
            await self._configure_and_receive(
                prescaler=4, channels=ch, sample_size=ss,
                sign_extend=se, left_justified=lj,
                avg_en=True, zcr_en=True,
                avgsel=avgsel, zcrsel=zcrsel,
                num_samples=2,
            )

    async def _ctrl_combos(self):
        """Sweep CTRL field combinations: enable, fifo_en, avg_en, zcr_en."""
        combos = [
            (False, False, False, False),
            (False, True, False, False),
            (False, False, True, False),
            (False, False, False, True),
            (True, True, False, False),
            (True, True, True, False),
            (True, True, False, True),
            (True, True, True, True),
            (True, False, True, True),
            (True, False, False, True),
            (True, False, True, False),
        ]
        for en, fifo, avg, zcr in combos:
            ctrl = 0
            if en:
                ctrl |= 1
            if fifo:
                ctrl |= 2
            if avg:
                ctrl |= 4
            if zcr:
                ctrl |= 8
            await self._w("ctrl_off", "CTRL", 0)
            await self._w("ctrl", "CTRL", ctrl)
            await self._r("ctrl_rd", "CTRL")

    async def _threshold_sweep(self):
        """Hit AVGT and ZCRT bins (16 bins, 4096 values each: 0-4095, 4096-8191, ...)."""
        if "AVGT" not in self.addr and "ZCRT" not in self.addr:
            return

        bin_reps = [v * 4096 + 100 for v in range(16)]

        if "AVGT" in self.addr:
            for v in bin_reps:
                await self._w("avgt", "AVGT", v)

        if "ZCRT" in self.addr:
            for v in bin_reps:
                await self._w("zcrt", "ZCRT", v)

    async def _fifo_and_flags(self):
        """Hit FIFO level bins and trigger AVG/ZCR/VAD flags."""
        await self._w("ctrl_off", "CTRL", 0)
        await self._w("pr", "PR", 2)

        # Set very low thresholds so flags trigger easily
        if "AVGT" in self.addr:
            await self._w("avgt_low", "AVGT", 0)
        if "ZCRT" in self.addr:
            await self._w("zcrt_low", "ZCRT", 0)

        cfg = 3 | (16 << 4) | (1 << 10) | (1 << 11)  # stereo, 16-bit, AVGSEL=1, ZCRSEL=1
        await self._w("cfg", "CFG", cfg)

        if "IM" in self.addr:
            await self._w("im", "IM", 0x3F)

        ctrl = 1 | 2 | 4 | 8  # enable + fifo + avg + zcr
        await self._w("ctrl", "CTRL", ctrl)

        bit_cyc = 3 * 2

        # Wait for FIFO to fill completely for high/full level bins
        await ClockCycles(self.dut.CLK, bit_cyc * 17 * 30)

        # Check flags — AVGF/ZCRF/VADF should be set now
        await self._r("ris_flags", "RIS")
        if "MIS" in self.addr:
            await self._r("mis_flags", "MIS")

        # FIFO high bin: read level when FIFO is full/nearly full
        if "RX_FIFO_LEVEL" in self.addr:
            await self._r("rx_lvl_full", "RX_FIFO_LEVEL")

        # Drain to mid level (drain ~8 samples from 16)
        for _ in range(4):
            await self._r("rxdata_drain", "RXDATA")
        if "RX_FIFO_LEVEL" in self.addr:
            await self._r("rx_lvl_mid", "RX_FIFO_LEVEL")

        # Drain to low level
        for _ in range(8):
            await self._r("rxdata_drain2", "RXDATA")
        if "RX_FIFO_LEVEL" in self.addr:
            await self._r("rx_lvl_low", "RX_FIFO_LEVEL")

        # Flush for empty
        if "RX_FIFO_FLUSH" in self.addr:
            await self._w("flush", "RX_FIFO_FLUSH", 1)
        if "RX_FIFO_LEVEL" in self.addr:
            await self._r("rx_lvl_empty", "RX_FIFO_LEVEL")
        await self._r("ris_empty", "RIS")

        # Clear interrupts and re-trigger AVG/ZCR/VAD
        if "IC" in self.addr:
            await self._w("ic", "IC", 0x3F)
        await self._r("ris_cleared", "RIS")

        # Re-enable and wait for flags to trigger again
        await self._w("ctrl_off", "CTRL", 0)
        ctrl_full = 1 | 2 | 4 | 8
        await self._w("ctrl_on", "CTRL", ctrl_full)
        await ClockCycles(self.dut.CLK, bit_cyc * 17 * 20)
        await self._r("ris_retrigger", "RIS")

    async def _channel_x_sample_size(self):
        """Ensure all channel x sample_size cross bins are hit."""
        for ch in [1, 2, 3]:
            for ss in [8, 16, 24, 32]:
                await self._configure_and_receive(
                    prescaler=4, channels=ch, sample_size=ss, num_samples=2,
                )

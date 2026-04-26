"""I2S configuration sequence — sets up prescaler, CFG, CTRL, FIFO, and interrupts."""

import random

from pyuvm import uvm_sequence, ConfigDB

from cf_verify.bus_env.bus_seq_lib import write_reg_seq, reset_seq


class i2s_config_seq(uvm_sequence):
    def __init__(self, name="i2s_config_seq", prescaler=None, channels=None,
                 sample_size=None, sign_extend=None, left_justified=None,
                 enable=True, fifo_en=True, avg_en=False, zcr_en=False,
                 im=None):
        super().__init__(name)
        self.prescaler = prescaler
        self.channels = channels
        self.sample_size = sample_size
        self.sign_extend = sign_extend
        self.left_justified = left_justified
        self.enable = enable
        self.fifo_en = fifo_en
        self.avg_en = avg_en
        self.zcr_en = zcr_en
        self.im = im

    async def body(self):
        await reset_seq("rst").start(self.sequencer)
        regs = ConfigDB().get(None, "", "bus_regs")
        addr = regs.reg_name_to_address

        # Enable clock gate
        if "GCLK" in addr:
            await write_reg_seq("wr_gclk", addr["GCLK"], 1).start(self.sequencer)

        # Disable I2S first
        await write_reg_seq("wr_ctrl_off", addr["CTRL"], 0).start(self.sequencer)

        # Prescaler
        pr = self.prescaler if self.prescaler is not None else random.randint(2, 8)
        await write_reg_seq("wr_pr", addr["PR"], pr).start(self.sequencer)

        # Configuration register
        ch = self.channels if self.channels is not None else random.choice([1, 2, 3])
        se = self.sign_extend if self.sign_extend is not None else 0
        lj = self.left_justified if self.left_justified is not None else 0
        ss = self.sample_size if self.sample_size is not None else random.choice([8, 16, 24, 32])
        cfg = ch | (se << 2) | (lj << 3) | (ss << 4)
        await write_reg_seq("wr_cfg", addr["CFG"], cfg).start(self.sequencer)

        # Interrupt mask
        im_val = self.im if self.im is not None else 0x3F
        if "IM" in addr:
            await write_reg_seq("wr_im", addr["IM"], im_val).start(self.sequencer)

        # Enable I2S
        ctrl = 0
        if self.enable:
            ctrl |= 1
        if self.fifo_en:
            ctrl |= 2
        if self.avg_en:
            ctrl |= 4
        if self.zcr_en:
            ctrl |= 8
        await write_reg_seq("wr_ctrl", addr["CTRL"], ctrl).start(self.sequencer)

"""WDT configuration sequence — sets load value, enables/disables the WDT."""

from pyuvm import uvm_sequence, ConfigDB

from cf_verify.bus_env.bus_seq_lib import write_reg_seq, reset_seq


class wdt_config_seq(uvm_sequence):
    def __init__(self, name="wdt_config_seq", load_value=0x100,
                 enable=True, im=None):
        super().__init__(name)
        self.load_value = load_value
        self.enable = enable
        self.im = im

    async def body(self):
        await reset_seq("rst").start(self.sequencer)

        regs = ConfigDB().get(None, "", "bus_regs")
        addr = regs.reg_name_to_address

        if "GCLK" in addr:
            await write_reg_seq("wr_gclk", addr["GCLK"], 1).start(self.sequencer)

        await write_reg_seq("wr_ctrl_off", addr["control"], 0).start(self.sequencer)

        await write_reg_seq("wr_load", addr["load"], self.load_value).start(
            self.sequencer
        )

        im_val = self.im if self.im is not None else 0x1
        if "IM" in addr:
            await write_reg_seq("wr_im", addr["IM"], im_val).start(self.sequencer)

        en_val = 1 if self.enable else 0
        await write_reg_seq("wr_ctrl", addr["control"], en_val).start(self.sequencer)

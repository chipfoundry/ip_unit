from uvm.seq import UVMSequence
from uvm.macros.uvm_object_defines import uvm_object_utils
from uvm.macros.uvm_message_defines import uvm_fatal
from EF_UVM.bus_env.bus_item import bus_item
from uvm.base.uvm_config_db import UVMConfigDb
from EF_UVM.bus_env.bus_seq_lib.bus_seq_base import bus_seq_base
from cocotb.triggers import Timer
from uvm.macros.uvm_sequence_defines import uvm_do_with, uvm_do
import random
from flash_seq_lib.flash_base_seq import flash_base_seq

class flash_rd_wr_seq(flash_base_seq):
    def __init__(self, name="flash_rd_wr_seq", memory_size=1024):
        super().__init__(name, memory_size)

    async def body(self):
        # send write requests as well. it should do nothing but we need to cover the effect
        await super().body()
        for _ in range(1000):
            address = random.randrange(0, self.memory_size - 4, 4)
            is_error = True if random.random() < 0.2 else False  # write 20% of the time
            await self.read_bulk(address=address, error=is_error)



uvm_object_utils(flash_rd_wr_seq)

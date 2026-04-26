from uvm.seq import UVMSequence
from uvm.macros.uvm_object_defines import uvm_object_utils
from uvm.macros.uvm_message_defines import uvm_fatal
from EF_UVM.bus_env.bus_item import bus_item
from uvm.base.uvm_config_db import UVMConfigDb
from EF_UVM.bus_env.bus_seq_lib.bus_seq_base import bus_seq_base
from cocotb.triggers import Timer
from uvm.macros.uvm_sequence_defines import uvm_do_with, uvm_do
import random
import cocotb


class flash_base_seq(bus_seq_base):

    def __init__(self, name="flash_async_reset_seq", memory_size=1024):
        super().__init__(name)
        self.memory_size = memory_size

    async def body(self):
        await super().body()

    async def read_bulk(self, address, error=False):
        bulk_size = random.randrange(3, 50)
        for _ in range(bulk_size):
            self.create_new_item()
            self.req.rand_mode(0)
            self.req.addr = address
            if error:
                self.req.kind = bus_item.WRITE
            else:
                self.req.kind = bus_item.READ
            self.req.data = 0  # needed to add any dummy value
            await uvm_do(self, self.req)
            address += 4
            if address >= self.memory_size:
                return


uvm_object_utils(flash_base_seq)

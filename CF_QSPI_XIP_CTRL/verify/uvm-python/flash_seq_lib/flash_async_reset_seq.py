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
from flash_seq_lib.flash_base_seq import flash_base_seq

class flash_async_reset_seq(flash_base_seq):

    def __init__(self, name="flash_async_reset_seq", memory_size=1024):
        super().__init__(name, memory_size)

    async def body(self):
        # get register names/address conversion dict
        await super().body()
        # await cocotb.start(self.send_async_reset())
        await self.read_rand_addresses()

    async def read_rand_addresses(self):
        for _ in range(500):
            address = random.randrange(0, self.memory_size, 4)
            await self.read_bulk(address=address)
            is_reset = True if random.random() < 0.1 else False
            if is_reset:
                rsp = []
                await self.get_response(rsp)
                await self.get_response(rsp)
                await self.send_nop()
                await self.send_reset()

    async def send_async_reset(self):
        while True:
            rand_time = random.randint(10000, 50000)
            await Timer(rand_time, "ns")  # wait random time for async reset
            await self.send_reset()


uvm_object_utils(flash_async_reset_seq)

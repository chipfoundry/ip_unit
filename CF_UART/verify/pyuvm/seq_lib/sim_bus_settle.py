"""Extra timing for bus register access under Verilator + Wishbone (cocotb sampling)."""

import os

from cocotb.triggers import ClockCycles, ReadOnly
from pyuvm import ConfigDB


def _bus_type() -> str:
    try:
        b = ConfigDB().get(None, "*", "BUS_TYPE")
    except Exception:
        b = None
    b = b or os.environ.get("BUS_TYPE", "")
    return (b or "").strip()


def is_verilator_wishbone() -> bool:
    return os.environ.get("SIM", "").lower() == "verilator" and _bus_type() == "WISHBONE"


async def after_reg_write(dut, cycles: int = 2) -> None:
    if is_verilator_wishbone() and cycles and cycles > 0:
        await ClockCycles(dut.CLK, cycles)


async def before_reg_read() -> None:
    await ReadOnly()

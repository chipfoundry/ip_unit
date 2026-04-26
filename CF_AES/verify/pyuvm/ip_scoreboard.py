"""AES scoreboard — compares DUT results against Python AES reference model."""

from pyuvm import uvm_root
from cf_verify.base.scoreboard import scoreboard
from ip_item.aes_item import aes_item

try:
    from Crypto.Cipher import AES as PyCryptoAES
    HAS_PYCRYPTO = True
except ImportError:
    HAS_PYCRYPTO = False


def _aes_reference(key_int, block_int, keylen, encdec):
    """Compute expected AES result using PyCryptodome."""
    if not HAS_PYCRYPTO:
        return None
    key_bytes_len = 32 if keylen == aes_item.KEY_256 else 16
    key_bytes = key_int.to_bytes(key_bytes_len, byteorder="little")
    block_bytes = block_int.to_bytes(16, byteorder="little")
    cipher = PyCryptoAES.new(key_bytes, PyCryptoAES.MODE_ECB)
    if encdec == aes_item.ENCRYPT:
        result_bytes = cipher.encrypt(block_bytes)
    else:
        result_bytes = cipher.decrypt(block_bytes)
    return int.from_bytes(result_bytes, byteorder="little")


class aes_scoreboard(scoreboard):
    def build_phase(self):
        super().build_phase()

    async def _compare_ip(self):
        """Compare AES results from DUT monitor against expected values."""
        while True:
            dut_tr = await self.ip_dut_fifo.get()
            ref_tr = await self.ip_ref_fifo.get()

            self.logger.info(
                f"AES SB: result=0x{dut_tr.result:032x} "
                f"ready={dut_tr.ready}"
            )

            self._check("IP", dut_tr, ref_tr)

    def check_phase(self):
        assert self.failed == 0, (
            f"AES scoreboard mismatches: failed={self.failed}, passed={self.passed}"
        )

    def report_phase(self):
        self.logger.info(
            f"AES Scoreboard: passed={self.passed}, failed={self.failed}"
        )

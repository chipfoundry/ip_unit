"""SHA-256 single-block hash test using NIST test vector.

NIST FIPS 180-4 test vector: SHA-256("abc")
Input: 0x61626380...00000018 (padded single block)
Expected: 0xba7816bf 8f01cfea 414140de 5dae2223
          b00361a3 96177a9c b410ff61 f20015ad
"""

import hashlib
from seq_lib.sha256_base_seq import sha256_base_seq

ABC_BLOCK = 0x61626380000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000018

EXPECTED_SHA256_ABC = int(hashlib.sha256(b"abc").hexdigest(), 16)


class sha256_single_block_seq(sha256_base_seq):
    async def body(self):
        await self._init()

        await self._hash(ABC_BLOCK, mode=1, is_first=True)

        digest = await self._read_digest_from_core()
        await self._read_digest()  # sample bus coverage

        await self._r("status", "STATUS")
        await self._r("ris", "RIS")

        assert digest == EXPECTED_SHA256_ABC, (
            f"SHA-256('abc') MISMATCH: "
            f"expected 0x{EXPECTED_SHA256_ABC:064x}, got 0x{digest:064x}"
        )

"""SHA-224 single-block hash test using NIST test vector.

SHA-224("abc") with padded block.
Expected: 0x23097d22 3405d822 8642a477 bda255b3
          2aadbce4 bda0b3f7 e36c9da7 (truncated to 224 bits)
"""

import hashlib
from seq_lib.sha256_base_seq import sha256_base_seq

ABC_BLOCK = 0x61626380000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000018

EXPECTED_SHA224_ABC = int(hashlib.sha224(b"abc").hexdigest(), 16)


class sha224_single_block_seq(sha256_base_seq):
    async def body(self):
        await self._init()

        await self._hash(ABC_BLOCK, mode=0, is_first=True)

        digest = await self._read_digest_from_core()
        await self._read_digest()

        await self._r("status", "STATUS")
        await self._r("ris", "RIS")

        digest_224 = digest >> 32
        assert digest_224 == EXPECTED_SHA224_ABC, (
            f"SHA-224('abc') MISMATCH: "
            f"expected 0x{EXPECTED_SHA224_ABC:056x}, got 0x{digest_224:056x}"
        )

"""SHA-256 multi-block hash test — exercises the 'next' command for chained blocks.

Uses a 2-block message to verify the init+next flow.
Message: "abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq" (448 bits)
This requires two 512-bit blocks after padding.
"""

import hashlib
from seq_lib.sha256_base_seq import sha256_base_seq

MSG = b"abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq"
EXPECTED = int(hashlib.sha256(MSG).hexdigest(), 16)

BLOCK0 = 0x6162636462636465636465666465666765666768666768696768696a68696a6b696a6b6c6a6b6c6d6b6c6d6e6c6d6e6f6d6e6f706e6f70718000000000000000

BLOCK1 = 0x000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001c0


class sha256_multi_block_seq(sha256_base_seq):
    async def body(self):
        await self._init()

        await self._hash(BLOCK0, mode=1, is_first=True)
        await self._hash(BLOCK1, mode=1, is_first=False)

        digest = await self._read_digest_from_core()
        await self._read_digest()

        await self._r("status", "STATUS")

        assert digest == EXPECTED, (
            f"SHA-256 multi-block MISMATCH: "
            f"expected 0x{EXPECTED:064x}, got 0x{digest:064x}"
        )

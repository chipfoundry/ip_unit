"""SHA256 interrupt sequence — exercises IRQ sources (valid, ready) and IM/IC."""

from seq_lib.sha256_base_seq import sha256_base_seq


ABC_BLOCK = 0x61626380000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000018


class sha256_interrupt_seq(sha256_base_seq):
    async def body(self):
        await self._init()

        await self._w("im_all", "IM", 0x3)

        await self._hash(ABC_BLOCK, mode=1, is_first=True)

        ris_val = await self._r("ris_valid", "RIS")
        assert ris_val is not None and (ris_val & 0x1), (
            f"SHA256 IRQ: RIS valid bit not set after hash, RIS=0x{ris_val if ris_val else 0:x}"
        )
        mis_val = await self._r("mis_valid", "MIS")
        assert mis_val is not None and (mis_val & 0x1), (
            f"SHA256 IRQ: MIS valid bit not set (IM=0x3), MIS=0x{mis_val if mis_val else 0:x}"
        )

        # Valid and ready are level-sensitive: IC write is accepted but
        # the RIS bit re-asserts while the source condition persists.
        # Verify through IM/MIS instead.
        await self._w("ic_valid", "IC", 0x1)
        await self._w("ic_ready", "IC", 0x2)

        await self._w("im_none", "IM", 0x0)
        mis_zero = await self._r("mis_zero", "MIS")
        assert mis_zero is not None and mis_zero == 0, (
            f"SHA256 IRQ: MIS not zero after disabling masks, MIS=0x{mis_zero if mis_zero else 0:x}"
        )

        for bit in range(2):
            await self._w(f"im_bit{bit}", "IM", 1 << bit)
            mis_bit = await self._r(f"mis_bit{bit}", "MIS")
            assert mis_bit is not None and (mis_bit & (1 << bit)), (
                f"SHA256 IRQ: MIS bit {bit} not set when IM bit {bit} enabled, MIS=0x{mis_bit if mis_bit else 0:x}"
            )

        await self._w("im_restore", "IM", 0x3)

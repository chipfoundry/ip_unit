"""QSPI coverage groups — address range and cache behavior bins.

Since this IP has no registers, coverage tracks AHB read address
distribution and cache hit/miss behavior.  Cache hits are inferred by
tracking previously-seen cache-line addresses (bus transactions do not
carry an explicit cache_hit flag).
"""

from cocotb_coverage.coverage import CoverPoint, CoverCross, coverage_db

CACHE_LINE_SIZE = 32


class qspi_cov_groups:
    def __init__(self, prefix):
        self.prefix = prefix
        self._seen_lines: set[int] = set()

        @CoverPoint(
            f"{prefix}.ahb_read_addr_range",
            xf=lambda tr: self._addr_bin(tr),
            bins=["low_4K", "mid_64K", "high_1M"],
        )
        def _addr_range(tr):
            pass

        @CoverPoint(
            f"{prefix}.cache_behavior",
            xf=lambda tr: self._cache_bin(tr),
            bins=["hit", "miss"],
        )
        def _cache_behavior(tr):
            pass

        self._addr_range = _addr_range
        self._cache_behavior = _cache_behavior

    def _addr_bin(self, tr):
        addr = getattr(tr, "addr", 0)
        if addr < 0x1000:
            return "low_4K"
        elif addr < 0x10000:
            return "mid_64K"
        return "high_1M"

    def _cache_bin(self, tr):
        """Infer cache hit/miss from repeated cache-line accesses."""
        if hasattr(tr, "cache_hit"):
            return "hit" if tr.cache_hit else "miss"
        addr = getattr(tr, "addr", 0)
        line = addr // CACHE_LINE_SIZE
        if line in self._seen_lines:
            return "hit"
        self._seen_lines.add(line)
        return "miss"

    def sample(self, tr):
        try:
            self._addr_range(tr)
            self._cache_behavior(tr)
        except Exception:
            pass

    def sample_bus(self, tr):
        self.sample(tr)

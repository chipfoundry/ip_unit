# CF_WDT32 Verification Issues

Issues found during verification are tracked below.

| # | Date | Severity | Description | Status |
|---|------|----------|-------------|--------|
| 1 | 2026-04 | High | IP scoreboard used `get_nowait()` and swallowed errors, so ref vs DUT IP compares rarely ran | Fixed — see `WDT_GAP_CLOSURE_REPORT.md` |

# CF_QSPI_XIP_CTRL — Verification traceability

## Registers

- This IP has **no memory-mapped configuration registers** in the usual sense; `WriteReadRegsTest` is not used. Verification is AHB read data vs loaded flash VIP model (`qspi_scoreboard`).

## Scoreboard

- **Bus path**: Compares read data to flash backing store; increments `failed` on mismatch.
- **check_phase**: Asserts zero mismatches.

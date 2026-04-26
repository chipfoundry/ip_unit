# CF_GPIO8 Gap Closure Report

## Issues Found and Fixed

### 1. Scoreboard never applied DIR/DATAO writes (critical)

- **Symptom**: Logs showed hundreds of `GPIO OE mismatch: expected 0x00, got 0xff` while tests still **passed** (no `check_phase` failure).
- **Cause**: `_update_shadow()` was dead code; pad checks used zero shadows.
- **Fix** (`ip_scoreboard.py`):
  - Override `_compare_bus` to mirror each completed **write** into `BusRegs` via `write_reg_value`.
  - `_compare_ip` uses `read_reg_value("dir")` / `read_reg_value("datao")` after `ReadOnly()` for deterministic ordering with RTL updates.
  - `check_phase`: `assert failed == 0` and `assert mismatch_count == 0`.

### 2. Weak register R/W check

- **Fix**: `WriteReadRegsTest` adds per-register write/read assertions (skips `IC`, `GCLK`, `*_FLUSH`).

### 3. Incomplete functional coverage (`reg.DATAO` bin `0xd0–0xdf`)

- **Fix**: Added `0xD8` to `gpio_coverage_closure_seq._data_sweep` data representatives.

### 4. Weak interrupt / edge checks

- **Fix**: `gpio_interrupt_seq` asserts `RIS`/`MIS` for pin-low and edge IRQ sections; `gpio_edge_detect_seq` asserts PE/NE bits in `RIS`.

### 5. IP item compare

- **Fix**: `gpio_item.do_compare` includes `is_input`.

## Final Metrics

| Metric | Result |
|--------|--------|
| Tests (APB+AHB+WB) | 27/27 pass |
| Functional coverage | 100% |

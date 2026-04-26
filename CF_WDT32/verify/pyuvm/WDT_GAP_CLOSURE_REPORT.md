# CF_WDT32 Gap Closure Report

## Finding: IP Scoreboard Did Not Compare DUT to Reference

The previous `wdt_scoreboard._compare_ip` used `ip_ref_fifo.get_nowait()` inside `try/except` and **ignored** failures. Reference predictions were almost never compared to DUT monitor transactions, so mismatches would not increment `failed` and tests could pass without exercising the scoreboard path.

## Fixes Applied

1. **`ip_scoreboard.py`**
   - `await self.ip_ref_fifo.get()` in lockstep with `await self.ip_dut_fifo.get()`.
   - Call `self._check("IP", dut_tr, ref_tr)` for every pair.
   - `check_phase`: `assert self.failed == 0`.
   - `report_phase`: logs `passed` / `failed` / timeout IRQ count.

2. **`test_lib.py` — `WriteReadRegsTest`**
   - Strict readback for wrapper registers that support read (`mode` not pure `"w"`).
   - Skips `IC`, `GCLK`, `*_FLUSH`, and core IP write-only regs (`load`, `control`).

3. **`seq_lib/wdt_interrupt_seq.py`**
   - Asserts timeout in `RIS` after wait.
   - Asserts `MIS` with `IM=1`, then `MIS==0` with `IM=0`, then `MIS` again after `IM` re-enabled.

## Metrics (After Changes)

| Metric | Result |
|--------|--------|
| Tests | 18/18 pass |
| Functional coverage | 100% (26/26 bins) |

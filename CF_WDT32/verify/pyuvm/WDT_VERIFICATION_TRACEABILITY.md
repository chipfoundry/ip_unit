# CF_WDT32 Verification Traceability

## Features → Coverage → Tests

| Feature | Registers / behavior | Coverage / checks | Tests |
|--------|----------------------|---------------------|-------|
| Loadable down-counter | `load`, `timer` | Auto `reg.*`, timer bins | `EnableDisableTest`, `ReloadTest`, closure |
| Enable / disable | `control` (WDTEN) | `reg.control`, enable paths | `EnableDisableTest`, closure |
| Timeout flag + IRQ | `RIS`/`MIS`/`IM`/`IC`, `irq` port | `IRQ.*`, `flag.*` | `TimeoutTest`, `InterruptTest`, `wdt_timeout_seq`, `wdt_interrupt_seq` |
| IP observability | IRQ edge → `wdt_item` | IP scoreboard `IP` compares | All tests that assert `irq` |

## Anti-Vacuous Measures

- **Scoreboard** (`ip_scoreboard.py`): Uses **lockstep** `await` on both `ip_dut_fifo` and `ip_ref_fifo` and `_check("IP", ...)`. Removed non-blocking `get_nowait()` + silent `except`, which skipped real compares. `check_phase` asserts `failed == 0`.
- **WriteReadRegsTest**: Asserted readback for **readable** writable wrapper registers (`mode != "w"` only); core `load`/`control` are write-only per YAML.
- **InterruptTest** (`wdt_interrupt_seq.py`): Asserts `RIS`/`MIS` after timeout and through IM mask on/off.

## Signoff

- Regression: **18/18** (6 tests × 3 buses).
- Functional coverage (merged): **100%**.

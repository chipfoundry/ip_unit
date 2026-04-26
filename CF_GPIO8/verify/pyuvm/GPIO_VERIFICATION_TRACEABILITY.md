# CF_GPIO8 Verification Traceability

## Feature → Coverage → Tests

| Feature | Registers / signals | Coverage | Tests / sequences |
|--------|---------------------|----------|-------------------|
| Register map | `DIR`, `DATAO`, `DATAI`, IRQ block | Auto `reg.*`, `flag.*` | `WriteReadRegsTest` (strict readback) |
| Direction per pin | `DIR` | `DIR.pin*`, `DIR.Pattern` | `DirectionTest`, `gpio_coverage_closure_seq` |
| Output drive | `DATAO`, `io_out`/`io_oe` | `Data.OUT`, `reg.DATAO` | `OutputTest`, closure `_data_sweep` |
| Input read | `DATAI`, `io_in` | `Data.IN` | `InputTest`, closure |
| Pin high/low flags | `RIS` bits 0–15 | `Flags.P*HI/LO`, `IRQ.P*HI/LO` | `InterruptTest`, `_pin_hi_lo_sweep` |
| Edge detect | `RIS` bits 16–31 | `Edge.P*PE/NE` | `EdgeDetectTest`, `_edge_sweep` |
| Interrupt path | `IM`, `MIS`, `RIS`, `IC` | `IRQ.*`, `flag.any_masked_irq` | `InterruptTest`, `_irq_sweep` |

## Anti-Vacuous Measures

- **Scoreboard**: Mirrors bus writes into `BusRegs` in `_compare_bus`, then compares pad `io_out`/`io_oe` to `DIR`/`DATAO` after `ReadOnly()`. `check_phase` asserts `failed == 0` and `mismatch_count == 0`.
- **WriteReadRegsTest**: Explicit asserted readback for each writable register (not log-only `write_read_regs_seq`).
- **Sequences**: Interrupt and edge tests assert expected `RIS`/`MIS` bits (not read-only).
- **`gpio_item.do_compare`**: Includes `is_input` for IP transaction equivalence.

## Signoff Status

- Regression: **27/27** (7 tests × 3 buses).
- Functional coverage: **100%** (merged `coverage_report.json`).

# CF_GPIO8 pyuvm Verification — Known Issues

## Open

- None at this time.

## Resolved

- **GPIO scoreboard vacuous pass (2026-04)**: Pad checks used uninitialized DIR/DATAO shadows; fixed by mirroring bus writes into `BusRegs` and asserting zero mismatches in `check_phase`. See `GPIO_GAP_CLOSURE_REPORT.md`.

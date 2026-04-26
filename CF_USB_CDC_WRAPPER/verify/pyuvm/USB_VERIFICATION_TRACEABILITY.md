# CF_USB_CDC_WRAPPER — Verification traceability

## Scoreboard

- **IP path**: USB CDC transactions compared in lockstep; `check_phase` asserts `failed == 0`.

## Register smoke

- **WriteReadRegsTest**: Standard sequence plus explicit readback for readable writable registers.

## Limits

- Full USB host/device protocol is not modeled; tests focus on wrapper registers, FIFOs, and PHY smoke as documented in `test_lib.py`.

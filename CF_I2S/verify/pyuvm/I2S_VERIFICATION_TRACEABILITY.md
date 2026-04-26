# CF_I2S — Verification traceability

## Scoreboard

- **IP path**: Lockstep sample compare; `check_phase` asserts `failed == 0`.

## Register smoke

- **WriteReadRegsTest**: `write_read_regs_seq` plus explicit readback for readable writable registers.

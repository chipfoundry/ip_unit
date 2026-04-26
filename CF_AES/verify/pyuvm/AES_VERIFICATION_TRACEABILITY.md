# CF_AES — Verification traceability

## Scoreboard

- **IP path**: `aes_scoreboard` pairs DUT and reference AES result items in lockstep.
- **check_phase**: `assert self.failed == 0`.
- Removed incorrect `match_count` increments when the reference FIFO was empty (would mask failures).

## Register smoke

- **WriteReadRegsTest**: `write_read_regs_seq` plus per-register write/read assert for readable writable registers (same skip list as other ChipFoundry IPs).

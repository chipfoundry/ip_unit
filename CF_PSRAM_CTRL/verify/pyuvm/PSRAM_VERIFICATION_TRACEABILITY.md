# CF_PSRAM_CTRL — Verification traceability

## Scoreboard

- There is **no** `ip_scoreboard` in this environment (`psram_env` uses ref model + coverage + logger). Bus/protocol checking relies on sequences, `MemoryReadWriteTest`, and optional `PSRAM_STRICT_MEMCHECK=1` for data integrity when the AHB read path matches the model.

## Registers

- Config addresses use **bit-field decoding**; many fields are write-only in RTL — `WriteReadRegsTest` verifies writes complete without bus errors rather than readback.

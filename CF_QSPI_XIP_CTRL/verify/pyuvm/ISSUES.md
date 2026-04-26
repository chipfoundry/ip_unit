# CF_QSPI_XIP_CTRL pyuvm Verification — Known Issues & Limitations

## Critical: No Registers

This IP has **zero registers** (`registers: []` in the YAML). The AHB bus interface
is the cache/memory read interface itself — every AHB read goes to the flash
controller, not to a register file.

**Impact:**
- `WriteReadRegsTest` (standard register verification) is **not applicable**
- `BusRegs` from `cf_verify` will load an empty register map
- No interrupt registers exist — `irq_exist` will be `False`
- Standard register coverage groups produce no bins

## Flash VIP Dependency

Full functional verification depends on the **SST26WF080B** Verilog flash model
located at `verify/vip/sst26wf080b.v`. This is a large vendor model (~2400 lines)
that provides cycle-accurate QSPI flash behavior.

**Impact:**
- The flash VIP must be compiled alongside the DUT for any read tests to work
- Memory must be loaded via hierarchical access (`vip.I0.memory[i]`) after
  elaboration — there is no standard `$readmemh` hook
- If the VIP access path changes (different simulator, different elaboration),
  tests that load flash memory will silently return X/0 data

## Controller Reset Sequence

After `HRESETn` deasserts, the controller automatically issues:
1. **Reset Enable** command (0x66)
2. **Reset Memory** command (0x99)

This takes `2 * (RESET_CYCLES + 1)` clock cycles (default: ~2000 clocks at
RESET_CYCLES=999). No AHB reads can complete until this sequence finishes.

**Impact:**
- Tests must wait at least ~2200 clock cycles after reset before issuing reads
- Premature reads will see `HREADYOUT=0` indefinitely

## Cache Verification Limitations

The Direct-Mapped Cache (DMC) behavior is not directly observable from the AHB
interface:

- **Cache hits** return data in 1 cycle (HREADYOUT stays 1)
- **Cache misses** stall HREADYOUT for `28 + 4*LINE_SIZE` cycles (default: 156 cycles)

Current test infrastructure observes miss/hit indirectly via:
1. Timing — HREADYOUT deassertion duration
2. Flash `ce_n` assertion count (monitored by `qspi_monitor`)

**Not yet verified:**
- Cache line eviction correctness (requires >NUM_LINES distinct line reads)
- Cache tag matching (requires careful address selection across index/tag ranges)
- Multi-word line fill ordering
- The `first` read after reset (which triggers the initial 0xEB command vs.
  subsequent continuous-read mode)

## Read-Only Interface

The controller ignores `HWRITE` — all AHB transactions are effectively reads.
Writing to the AHB interface has no effect (no error, no response).

**Impact:**
- No write verification is possible or needed
- AHB protocol coverage for writes is N/A

## Functional Coverage Gaps

Due to the register-less architecture, functional coverage is limited to:
- AHB read address range bins (low/mid/high/top)
- Cache hit/miss behavioral bins (inferred, not directly observable)

**Not covered:**
- Register field coverage (N/A — no registers)
- Interrupt coverage (N/A — no interrupts)
- Configuration parameter sweep (NUM_LINES, LINE_SIZE, RESET_CYCLES are
  compile-time parameters, not runtime configurable)

## Compilation Sensitivity

The SST26WF080B VIP uses constructs that may not be supported by all simulators:
- `inout` tri-state SIO bus
- `$readmemh` for memory initialization
- Large memory arrays (1MB)

Verilator in particular may have issues with the tri-state `SIO` bus.
Icarus Verilog is the recommended simulator for this IP.

## What Full Verification Would Require

1. **Cycle-accurate flash read model** — verify every byte of cache line fill
   matches the flash memory contents
2. **Cache tag/index/offset decomposition checker** — verify the cache correctly
   maps addresses to lines
3. **Performance model** — verify hit latency (1 cycle) and miss latency
   (28 + 4*LINE_SIZE cycles)
4. **Reset sequence protocol checker** — decode the SPI commands sent during
   reset and verify 0x66/0x99 command sequence
5. **Continuous read mode verification** — verify the initial 0xEB command
   establishes continuous read mode, and subsequent reads skip the command byte

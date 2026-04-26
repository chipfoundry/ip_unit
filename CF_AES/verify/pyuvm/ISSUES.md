# CF_AES Verification Issues

## CRITICAL: RESULT register multi-driver bug

**Severity:** Critical — AES results cannot be read back via the bus interface.

The generated bus wrappers (CF_AES_APB.v, CF_AES_AHBL.v, CF_AES_WB.v) declare
RESULT0–RESULT3 as writable registers and drive the `result[127:0]` wire from
them:

```verilog
reg [31:0] RESULT0_REG;
assign result[31:0] = RESULT0_REG;
```

However, `aes_core` declares `result` as an **output** port:

```verilog
output wire [127:0] result
```

This creates a **multi-driver conflict** on the `result` net. In simulation
(Icarus/Verilator) the result wire resolves to `X` because both the register
assigns and the aes_core output drive it simultaneously.

**Impact:**
- Reading RESULT0–RESULT3 via the bus returns whatever was last **written**
  to those addresses — not the actual AES computation output.
- The `result` input to `aes_core` is corrupted (X) which may interfere
  with internal state.

**Root cause:** The YAML register spec marks RESULT0–RESULT3 as `mode: w`
with `write_port: result[…]`. The code generator treats them as write-only
registers that drive the named port. But for AES, `result` is an **output**
from the core, not an input.

**Fix required in bus wrappers:**
1. Remove `assign result[…] = RESULT_REG` statements.
2. Instead, capture aes_core output into RESULT registers:
   ```verilog
   always @(posedge clk)
     if (result_valid) RESULT0_REG <= result[31:0];
   ```
3. Or fix the YAML to declare RESULT registers as `mode: r` with
   `read_port: result[…]`.

**Workaround in verification:**
The testbench (`top.v`) exposes `dut.instance_to_wrap.result` as
`aes_result` at the top level, allowing the monitor and sequences to
read the true aes_core output via hierarchical access.

---

## MODERATE: ef_util_gating_cell naming mismatch

The bus wrappers instantiate `ef_util_gating_cell` but the vendored
CF_IP_UTIL library (`cf_util_lib.v`) defines `cf_util_gating_cell`.

**Workaround:** `top.v` provides a stub `ef_util_gating_cell` module that
passes the clock through for simulation.

---

## MINOR: AHBL init/next pulsing inconsistency

The AHBL wrapper pulses `init` and `next` for one clock cycle after a CTRL
write (via `valid_ctrl_wr` state machine). The APB and WB wrappers drive
`init`/`next` directly from `CTRL_REG` bits — they stay asserted until
cleared by software.

This means the AES operation sequence differs between bus types:
- **AHBL:** Write CTRL once; init/next auto-deassert.
- **APB/WB:** Write CTRL with init=1, then write again with init=0.

The verification sequences handle both cases by explicitly clearing
the init/next bits after setting them.

---

## MINOR: STATUS_WIRE uninitialized bits

`STATUS_WIRE` is declared as `wire [7:0]` but only bits 6 (ready) and 7
(result_valid) are assigned. Bits [5:0] are undriven and will read as `X`
in simulation (or `Z` depending on the simulator).

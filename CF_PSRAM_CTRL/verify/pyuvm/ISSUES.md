# CF_PSRAM_CTRL pyuvm Verification — Known Issues & Limitations

## 1. No PSRAM Memory Model

Full memory-access verification (read/write to PSRAM address space 0x00000000–0x00700000)
requires a behavioral PSRAM Verilog model (e.g. `verify/models/23LC1024.v`; legacy `verify/utb/` removed).
`verify/uvm-python/` directory). Without it, the external SPI/QSPI/QPI data lines
(`din`) are not driven with meaningful responses, so:

- Memory write/read-back tests cannot verify data integrity
- SPI protocol timing and framing cannot be fully checked
- The IP monitor captures transaction boundaries (ce_n edges) but cannot decode data

**Resolution:** Integrate the M23LC1024.v model into top.v and add memory-access
test sequences.

## 2. High Register Offsets (>0x00800000)

The PSRAM controller uses address-bit decoding for configuration registers:

| Register    | Offset       | Address Bit |
|-------------|-------------|-------------|
| rd_cmd      | 0x00800100  | HADDR[8]    |
| wr_cmd      | 0x00800200  | HADDR[9]    |
| eqpi_cmd    | 0x00800400  | HADDR[10]   |
| xqpi_cmd    | 0x00800800  | HADDR[11]   |
| wait_states | 0x00801000  | HADDR[12]   |
| mode        | 0x00802000  | HADDR[13]   |
| enter_qpi   | 0x00804000  | HADDR[14]   |
| exit_qpi    | 0x00808000  | HADDR[15]   |

The `cf_verify.bus_env.bus_regs.BusRegs` class parses these offsets correctly from
the YAML, but the standard `write_read_regs_seq` may not work because:

- These registers are **write-only** (the RTL has no read-back mux for config registers)
- The `data_cfg` signal in the wrapper distinguishes config accesses (HADDR[23]=0)
  from memory accesses (HADDR[23]=1), and config writes at these addresses set
  `last_data_cfg = ~last_HADDR[23] = 0` which enters the config branch
- Read-back of these registers returns whatever the PSRAM data_o bus has, not the
  register values

The custom `WriteReadRegsTest` handles this by only verifying that writes complete
without hanging (HREADYOUT returns to 1).

## 3. Write-Only Registers

All 8 configuration registers in this IP are write-only. There is no read-back
path in the RTL — attempting to read from a config register address will return
data from the PSRAM's data_o signal (which is undefined without a PSRAM model).

This means:
- Traditional write-then-read register testing cannot verify values
- The reference model tracks shadow registers for internal consistency only
- Verification relies on observing side-effects (SPI commands, mode changes)

## 4. AHBL-Only Bus Interface

This IP only supports AHB-Lite (AHBL). There are no APB or Wishbone wrappers.
The test runner is configured with `BUSES = ["AHB"]` only.

## 5. No Interrupts

This IP has no interrupt/flag infrastructure. The `irq_exist` config is set to
`False` and no IRQ-related tests are included.

## 6. No FIFOs

This IP has no FIFO infrastructure. Data passes directly through the SPI controller.

# CF_USB_CDC_WRAPPER — Known Issues

## Fixed RTL Compilation Errors

### 1. APB Wrapper: Missing `usb_cdc_clk_48MHz` Port — FIXED
**File:** `hdl/rtl/bus_wrappers/CF_USB_CDC_WRAPPER_APB.v`

Added `input wire usb_cdc_clk_48MHz` to the APB wrapper module ports and connected
it through to the inner `usb_cdc_wrapper` instantiation. Also applied the same fix
to the `.dev.v` variant and `verify/pyuvm/top.v`.

### 2. APB/AHB Wrappers: Undefined Localparam Names — FIXED
**Files:** `CF_USB_CDC_WRAPPER_APB.v`, `CF_USB_CDC_WRAPPER_AHBL.v`, and `.dev.v` variants

Renamed `IM_REG_OFFSET`, `MIS_REG_OFFSET`, `RIS_REG_OFFSET`, `ICR_REG_OFFSET` to
`IM_REG_ADDR`, `MIS_REG_ADDR`, `RIS_REG_ADDR`, `ICR_REG_ADDR` to match their usage
in register write logic and PRDATA/HRDATA read-back muxes.

### 3. AHB Wrapper: Width Mismatch on `RIS_REG` Reset — FIXED
**File:** `hdl/rtl/bus_wrappers/CF_USB_CDC_WRAPPER_AHBL.v`

Changed `RIS_REG` reset value from `32'd0` to `6'd0` to match the 6-bit register width.

## Remaining Verification Limitations

### 4. No USB Protocol-Level Testing
The pyuvm verification environment focuses on register-level and FIFO-level testing.
Protocol-level USB verification (enumeration, bulk transfers, CDC class requests)
requires a USB host BFM which is not included. Legacy Verilog loopback under `verify/utb/` was removed; see **`UsbPhySmokeTest`** in `test_lib.py` for minimal PHY sanity after reset.
testbench provides some protocol-level coverage using Verilog tasks.

### 5. RX FIFO Cannot Be Filled via Bus
The RX FIFO is filled by the USB CDC core receiving data from the USB bus. Without a
working USB host model driving dp_rx_i/dn_rx_i with valid USB packets, the RX FIFO
remains empty during register-level tests. This limits RX FIFO level and RXA/RXF flag
testing.

### 6. Dependency Management
The `usb_cdc` IP core must be cloned manually:
```
cd CF_USB_CDC_WRAPPER && git clone https://github.com/efabless/usb_cdc.git ip/usb_cdc
```
The `ip/dependencies.json` references it but `ipm` cannot resolve it automatically
from chipfoundry.

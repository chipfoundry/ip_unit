`timescale 1ns/1ps

module top();
    reg     CLK = 0;
    reg     RESETn = 0;

    // USB D+/D- signals
    reg     dp_rx_i = 1;
    reg     dn_rx_i = 0;
    wire    dp_pu_o;
    wire    dp_tx_o;
    wire    dn_tx_o;
    wire    tx_en_o;
    wire    irq;

    `ifdef BUS_TYPE_APB
        wire        PCLK = CLK;
        wire        usb_cdc_clk_48MHz = CLK;
        wire        PRESETn = RESETn;
        wire [31:0] PADDR;
        wire        PWRITE;
        wire        PSEL;
        wire        PENABLE;
        wire [31:0] PWDATA;
        wire [31:0] PRDATA;
        wire        PREADY;
        usb_cdc_wrapper_apb dut(
            .dp_pu_o(dp_pu_o),
            .dp_rx_i(dp_rx_i),
            .dn_rx_i(dn_rx_i),
            .dp_tx_o(dp_tx_o),
            .dn_tx_o(dn_tx_o),
            .tx_en_o(tx_en_o),
            .PCLK(PCLK),
            .usb_cdc_clk_48MHz(usb_cdc_clk_48MHz),
            .PRESETn(PRESETn),
            .PADDR(PADDR),
            .PWRITE(PWRITE),
            .PSEL(PSEL),
            .PENABLE(PENABLE),
            .PWDATA(PWDATA),
            .PRDATA(PRDATA),
            .PREADY(PREADY),
            .irq(irq)
        );
    `endif

    `ifdef BUS_TYPE_AHB
        wire        HCLK = CLK;
        wire        usb_cdc_clk_48MHz = CLK;
        wire        HRESETn = RESETn;
        wire [31:0] HADDR;
        wire        HWRITE;
        reg         HSEL = 0;
        wire        HREADYOUT;
        reg  [1:0]  HTRANS = 0;
        reg  [2:0]  HSIZE = 3'b010;
        wire [31:0] HWDATA;
        wire [31:0] HRDATA;
        reg         HREADY = 1;
        usb_cdc_wrapper_ahbl dut(
            .dp_pu_o(dp_pu_o),
            .dp_rx_i(dp_rx_i),
            .dn_rx_i(dn_rx_i),
            .dp_tx_o(dp_tx_o),
            .dn_tx_o(dn_tx_o),
            .tx_en_o(tx_en_o),
            .HCLK(HCLK),
            .usb_cdc_clk_48MHz(usb_cdc_clk_48MHz),
            .HRESETn(HRESETn),
            .HADDR(HADDR),
            .HWRITE(HWRITE),
            .HTRANS(HTRANS),
            .HREADY(HREADY),
            .HSEL(HSEL),
            .HSIZE(HSIZE),
            .HWDATA(HWDATA),
            .HRDATA(HRDATA),
            .HREADYOUT(HREADYOUT),
            .irq(irq)
        );
    `endif

    initial begin
        #100 RESETn = 1;
    end

    `ifndef SKIP_WAVE_DUMP
        initial begin
            $dumpfile({"waves.vcd"});
            $dumpvars(0, top);
        end
    `endif
    always #10 CLK = !CLK;
endmodule

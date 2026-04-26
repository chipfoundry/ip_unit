`timescale 1ns/1ps

/*
   Stub for ef_util_gating_cell — the bus wrappers instantiate this name
   but the vendored CF_IP_UTIL provides cf_util_gating_cell instead.
   For simulation we simply pass the clock through.
*/
module ef_util_gating_cell(
    input  wire clk,
    input  wire clk_en,
    output wire clk_o
);
    assign clk_o = clk;
endmodule

module top();
    reg     CLK = 0;
    reg     RESETn = 0;
    wire    irq;

    `ifdef BUS_TYPE_APB
        wire        PCLK    = CLK;
        wire        PRESETn = RESETn;
        wire [31:0] PADDR;
        wire        PWRITE;
        wire        PSEL;
        wire        PENABLE;
        wire [31:0] PWDATA;
        wire [31:0] PRDATA;
        wire        PREADY;
        CF_AES_APB dut(
            .PCLK(PCLK), .PRESETn(PRESETn),
            .PADDR(PADDR), .PWRITE(PWRITE), .PSEL(PSEL),
            .PENABLE(PENABLE), .PWDATA(PWDATA), .PRDATA(PRDATA),
            .PREADY(PREADY), .IRQ(irq)
        );
    `endif

    `ifdef BUS_TYPE_AHB
        wire        HCLK     = CLK;
        wire        HRESETn  = RESETn;
        wire [31:0] HADDR;
        wire        HWRITE;
        reg         HSEL     = 0;
        wire        HREADYOUT;
        reg  [ 1:0] HTRANS   = 0;
        wire [31:0] HWDATA;
        wire [31:0] HRDATA;
        reg         HREADY   = 1;
        CF_AES_AHBL dut(
            .HCLK(HCLK), .HRESETn(HRESETn),
            .HADDR(HADDR), .HWRITE(HWRITE), .HSEL(HSEL),
            .HTRANS(HTRANS), .HWDATA(HWDATA), .HRDATA(HRDATA),
            .HREADY(HREADY), .HREADYOUT(HREADYOUT), .IRQ(irq)
        );
    `endif

    `ifdef BUS_TYPE_WISHBONE
        wire        clk_i  = CLK;
        wire        rst_i  = ~RESETn;
        wire [31:0] adr_i;
        wire [31:0] dat_i;
        wire [31:0] dat_o;
        wire [ 3:0] sel_i;
        wire        cyc_i;
        wire        stb_i;
        wire        we_i;
        wire        ack_o;
        CF_AES_WB dut(
            .clk_i(clk_i), .rst_i(rst_i),
            .adr_i(adr_i), .dat_i(dat_i), .dat_o(dat_o),
            .sel_i(sel_i), .cyc_i(cyc_i), .stb_i(stb_i),
            .we_i(we_i), .ack_o(ack_o), .IRQ(irq)
        );
    `endif

    // Read aes_core internal signals directly to bypass the multi-driver
    // bug on the 'result' port (bus wrapper RESULT_REG also drives it).
`ifndef GL
    wire [127:0] aes_result       = dut.instance_to_wrap.muxed_new_block;
    wire         aes_result_valid  = dut.instance_to_wrap.result_valid_reg;
    wire         aes_ready         = dut.instance_to_wrap.ready_reg;
`else
    wire [127:0] aes_result       = 128'b0;
    wire         aes_result_valid  = 1'b0;
    wire         aes_ready         = 1'b0;
`endif

    initial begin
        #100 RESETn = 1;
    end

    `ifndef SKIP_WAVE_DUMP
        initial begin
            $dumpfile("waves.vcd");
            $dumpvars(0, top);
        end
    `endif

    always #10 CLK = !CLK;
endmodule

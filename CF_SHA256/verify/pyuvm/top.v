`timescale 1ns/1ps

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
        CF_SHA256_APB dut(
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
        CF_SHA256_AHBL dut(
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
        CF_SHA256_WB dut(
            .clk_i(clk_i), .rst_i(rst_i),
            .adr_i(adr_i), .dat_i(dat_i), .dat_o(dat_o),
            .sel_i(sel_i), .cyc_i(cyc_i), .stb_i(stb_i),
            .we_i(we_i), .ack_o(ack_o), .IRQ(irq)
        );
    `endif

`ifndef GL
    // Read H-registers directly to bypass multi-driver bug on 'digest' port
    wire [255:0] sha_digest       = {
        dut.instance_to_wrap.H0_reg, dut.instance_to_wrap.H1_reg,
        dut.instance_to_wrap.H2_reg, dut.instance_to_wrap.H3_reg,
        dut.instance_to_wrap.H4_reg, dut.instance_to_wrap.H5_reg,
        dut.instance_to_wrap.H6_reg, dut.instance_to_wrap.H7_reg
    };
    wire         sha_digest_valid  = dut.instance_to_wrap.digest_valid_reg;
    wire         sha_ready         = dut.instance_to_wrap.ready_flag;
`else
    wire [255:0] sha_digest       = 256'b0;
    wire         sha_digest_valid  = 1'b0;
    wire         sha_ready         = 1'b0;
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

`timescale 1ns/1ps

module top();
    reg     CLK = 0;
    reg     RESETn = 0;
    reg  [7:0] io_in = 8'h00;
    wire [7:0] io_out;
    wire [7:0] io_oe;
    wire       irq;

    `ifdef BUS_TYPE_APB
        wire        PCLK = CLK;
        wire        PRESETn = RESETn;
        wire [31:0] PADDR;
        wire        PWRITE;
        wire        PSEL;
        wire        PENABLE;
        wire [31:0] PWDATA;
        wire [31:0] PRDATA;
        wire        PREADY;
        CF_GPIO8_APB dut(
            .io_in(io_in), .io_out(io_out), .io_oe(io_oe),
            .PCLK(PCLK), .PRESETn(PRESETn),
            .PADDR(PADDR), .PWRITE(PWRITE), .PSEL(PSEL),
            .PENABLE(PENABLE), .PWDATA(PWDATA), .PRDATA(PRDATA),
            .PREADY(PREADY), .IRQ(irq)
        );
    `endif

    `ifdef BUS_TYPE_AHB
        wire        HCLK = CLK;
        wire        HRESETn = RESETn;
        reg  [31:0] HADDR = 0;
        reg         HWRITE = 0;
        reg         HSEL = 0;
        wire        HREADYOUT;
        reg  [1:0]  HTRANS = 0;
        reg  [31:0] HWDATA = 0;
        wire [31:0] HRDATA;
        reg         HREADY = 1;
        CF_GPIO8_AHBL dut(
            .io_in(io_in), .io_out(io_out), .io_oe(io_oe),
            .HCLK(HCLK), .HRESETn(HRESETn),
            .HADDR(HADDR), .HWRITE(HWRITE), .HSEL(HSEL),
            .HTRANS(HTRANS), .HWDATA(HWDATA), .HRDATA(HRDATA),
            .HREADY(HREADY), .HREADYOUT(HREADYOUT), .IRQ(irq)
        );
    `endif

    `ifdef BUS_TYPE_WISHBONE
        wire        clk_i = CLK;
        wire        rst_i = ~RESETn;
        wire [31:0] adr_i;
        wire [31:0] dat_i;
        wire [31:0] dat_o;
        wire [3:0]  sel_i;
        wire        cyc_i;
        wire        stb_i;
        wire        we_i;
        wire        ack_o;
        CF_GPIO8_WB dut(
            .io_in(io_in), .io_out(io_out), .io_oe(io_oe),
            .clk_i(clk_i), .rst_i(rst_i),
            .adr_i(adr_i), .dat_i(dat_i), .dat_o(dat_o),
            .sel_i(sel_i), .cyc_i(cyc_i), .stb_i(stb_i),
            .we_i(we_i), .ack_o(ack_o), .IRQ(irq)
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

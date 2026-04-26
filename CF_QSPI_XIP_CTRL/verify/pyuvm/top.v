`timescale 1ns/1ps

module top();
    reg         HCLK = 0;
    reg         HRESETn = 0;

    wire        CLK = HCLK;
    wire        RESETn = HRESETn;

    wire [31:0] HADDR;
    wire        HWRITE;
    reg         HSEL = 0;
    wire        HREADYOUT;
    reg  [1:0]  HTRANS = 0;
    wire [31:0] HRDATA;
    wire        HREADY;

    wire        sck;
    wire        ce_n;
    wire [3:0]  din;
    wire [3:0]  dout;
    wire [3:0]  douten;

    CF_QSPI_XIP_CTRL_AHBL dut(
        .HCLK(HCLK),
        .HRESETn(HRESETn),
        .HADDR(HADDR),
        .HWRITE(HWRITE),
        .HSEL(HSEL),
        .HTRANS(HTRANS),
        .HRDATA(HRDATA),
        .HREADY(HREADY),
        .HREADYOUT(HREADYOUT),
        .sck(sck),
        .ce_n(ce_n),
        .din(din),
        .dout(dout),
        .douten(douten)
    );

    assign HREADY = HREADYOUT;

    wire [3:0] SIO;
    assign SIO = (douten == 4'b1111) ? dout : 4'bzzzz;
    assign din = SIO;

    sst26wf080b vip(
        .SCK(sck),
        .CEb(ce_n),
        .SIO(SIO)
    );

    initial begin
        #100 HRESETn = 1;
    end

    `ifndef SKIP_WAVE_DUMP
        initial begin
            $dumpfile({"waves.vcd"});
            $dumpvars(0, top);
        end
    `endif

    always #10 HCLK = !HCLK;
endmodule

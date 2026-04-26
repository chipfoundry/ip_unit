`timescale 1ns/1ps

module top();
    reg     CLK = 0;
    reg     RESETn = 0;

    wire [3:0]  din;
    wire [3:0]  dout;
    wire [3:0]  douten;
    wire        sck;
    wire        ce_n;

    // Bidirectional quad lines — match legacy AHBL TB (HOLD/SIO3 weak pull-up when idle)
    wire [3:0] dio;
    assign dio[0] = douten[0] ? dout[0] : 1'bz;
    assign dio[1] = douten[1] ? dout[1] : 1'bz;
    assign dio[2] = douten[2] ? dout[2] : 1'bz;
    assign dio[3] = douten[3] ? dout[3] : douten[0] ? 1'b1 : 1'bz;

    // M23LC1024 SRAM behavioral model for memory-access verification
    M23LC1024 sram (
        .SI_SIO0(dio[0]),
        .SO_SIO1(dio[1]),
        .SIO2(dio[2]),
        .HOLD_N_SIO3(dio[3]),
        .SCK(sck),
        .CS_N(ce_n),
        .RESET(~RESETn)
    );

    assign din = dio;

    `ifdef BUS_TYPE_AHB
        wire        HCLK = CLK;
        wire        HRESETn = RESETn;
        reg  [31:0] HADDR = 0;
        reg         HWRITE = 0;
        reg         HSEL = 0;
        wire        HREADYOUT;
        reg  [1:0]  HTRANS = 0;
        reg  [2:0]  HSIZE = 3'b010;  // default: word-size transfers
        reg  [31:0] HWDATA = 0;
        wire [31:0] HRDATA;
        reg         HREADY = 1;

        CF_PSRAM_CTRL_AHBL dut(
            .HCLK(HCLK),
            .HRESETn(HRESETn),
            .HSEL(HSEL),
            .HADDR(HADDR),
            .HWDATA(HWDATA),
            .HTRANS(HTRANS),
            .HSIZE(HSIZE),
            .HWRITE(HWRITE),
            .HREADY(HREADY),
            .HREADYOUT(HREADYOUT),
            .HRDATA(HRDATA),
            .sck(sck),
            .ce_n(ce_n),
            .din(din),
            .dout(dout),
            .douten(douten)
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

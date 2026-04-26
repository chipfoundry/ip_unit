
/*
 Copyright 2024 Efabless Corp.
 
 Author: Efabless Corp. (ip_admin@efabless.com)
 
 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at
 
 http://www.apache.org/licenses/LICENSE-2.0
 
 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
 
 */



`timescale			1ns/1ns
`default_nettype	none





module usb_cdc_wrapper_ahbl (
	output	wire 		dp_pu_o,
	input	wire 		dp_rx_i,
	input	wire 		dn_rx_i,
	output	wire 		dp_tx_o,
	output	wire 		dn_tx_o,
	output	wire 		tx_en_o,
	input	wire 		HCLK,
	input   wire        usb_cdc_clk_48MHz,
	input	wire 		HRESETn,
	input	wire [31:0]	HADDR,
	input	wire 		HWRITE,
	input	wire [1:0]	HTRANS,
	input	wire 		HREADY,
	input	wire 		HSEL,
	input	wire [2:0]	HSIZE,
	input	wire [31:0]	HWDATA,
	output	wire [31:0]	HRDATA,
	output	wire 		HREADYOUT,
	output	wire 		irq
);
	localparam[15:0] TXDATA_REG_ADDR = 16'h0000;
	localparam[15:0] RXDATA_REG_ADDR = 16'h0004;
	localparam[15:0] TXFIFOLEVEL_REG_ADDR = 16'h0008;
	localparam[15:0] RXFIFOLEVEL_REG_ADDR = 16'h000c;
	localparam[15:0] TXFIFOT_REG_ADDR = 16'h0010;
	localparam[15:0] RXFIFOT_REG_ADDR = 16'h0014;
	localparam[15:0] CONTROL_REG_ADDR = 16'h0018;
	localparam[15:0] IM_REG_ADDR = 16'hff00;
	localparam[15:0] MIS_REG_ADDR = 16'hff04;
	localparam[15:0] RIS_REG_ADDR = 16'hff08;
	localparam[15:0] ICR_REG_ADDR = 16'hff0c;
	localparam[15:0] CG_REG_ADDR = 16'h0f80;

	reg             last_HSEL;
	reg [31:0]      last_HADDR;
	reg             last_HWRITE;
	reg [1:0]       last_HTRANS;

	always@ (posedge HCLK or negedge HRESETn) begin
		if (!HRESETn) begin
			last_HSEL       <= 0;
			last_HADDR      <= 0;
			last_HWRITE     <= 0;
			last_HTRANS     <= 0;
		end else if (HREADY) begin
			last_HSEL       <= HSEL;
			last_HADDR      <= HADDR;
			last_HWRITE     <= HWRITE;
			last_HTRANS     <= HTRANS;
		end
	end

	reg	[3:0]	TXFIFOT_REG;
	reg	[3:0]	RXFIFOT_REG;
	reg	[0:0]	CONTROL_REG;
	reg	[5:0]	RIS_REG;
	reg	[5:0]	ICR_REG;
	reg	[5:0]	IM_REG;
	reg	[0:0]	CG_REG;

	wire[7:0]	rx_fifo_rdata;
	wire[7:0]	RXDATA_REG	= rx_fifo_rdata;
	wire[3:0]	tx_fifo_level;
	wire[3:0]	TXFIFOLEVEL_REG	= tx_fifo_level;
	wire[3:0]	rx_fifo_level;
	wire[3:0]	RXFIFOLEVEL_REG	= rx_fifo_level;
	wire[3:0]	tx_fifo_th	= TXFIFOT_REG[3:0];
	wire[3:0]	rx_fifo_th	= RXFIFOT_REG[3:0];
	wire		en	= CONTROL_REG[0:0];
	wire		tx_fifo_empty;
	wire		_TX_EMPTY_FLAG_FLAG_	= tx_fifo_empty;
	wire		tx_fifo_level_below;
	wire		_TX_BELOW_FLAG_FLAG_	= tx_fifo_level_below;
	wire		rx_fifo_full;
	wire		_RX_FULL_FLAG_FLAG_	= rx_fifo_full;
	wire		rx_fifo_level_above;
	wire		_RX_ABOVE_FLAG_FLAG_	= rx_fifo_level_above;
	wire		rx_fifo_empty;
	wire		_RX_EMPTY_FLAG_FLAG_	= rx_fifo_empty;
	wire		tx_fifo_full;
	wire		_TX_FULL_FLAG_FLAG_	= tx_fifo_full;
	wire[5:0]	MIS_REG	= RIS_REG & IM_REG;
	wire		ahbl_valid	= last_HSEL & last_HTRANS[1];
	wire		ahbl_we	= last_HWRITE & ahbl_valid;
	wire		ahbl_re	= ~last_HWRITE & ahbl_valid;
	wire		_gclk_;
	wire		_clk_	= HCLK;
	wire		_rst_	= ~HRESETn;
	wire		rx_fifo_rd	= (ahbl_re & (last_HADDR[15:0]==RXDATA_REG_ADDR));
	wire		tx_fifo_wr	= (ahbl_we & (last_HADDR[15:0]==TXDATA_REG_ADDR));
	wire[7:0]	tx_fifo_wdata	= HWDATA[7:0];

	assign _gclk_ = _clk_;

	usb_cdc_wrapper inst_to_wrap (
		.clk(_gclk_),
		.usb_cdc_clk_48MHz(usb_cdc_clk_48MHz),
		.rst_n(~_rst_),
		.rx_fifo_rd(rx_fifo_rd),
		.rx_fifo_full(rx_fifo_full),
		.rx_fifo_empty(rx_fifo_empty),
		.rx_fifo_level(rx_fifo_level),
		.rx_fifo_rdata(rx_fifo_rdata),
		.rx_fifo_th(rx_fifo_th),
		.rx_fifo_level_above(rx_fifo_level_above),
		.tx_fifo_wr(tx_fifo_wr),
		.tx_fifo_full(tx_fifo_full),
		.tx_fifo_empty(tx_fifo_empty),
		.tx_fifo_level(tx_fifo_level),
		.tx_fifo_wdata(tx_fifo_wdata),
		.tx_fifo_th(tx_fifo_th),
		.tx_fifo_level_below(tx_fifo_level_below),
		.dp_pu_o(dp_pu_o),
		.dp_rx_i(dp_rx_i),
		.dn_rx_i(dn_rx_i),
		.dp_tx_o(dp_tx_o),
		.dn_tx_o(dn_tx_o),
		.tx_en_o(tx_en_o)
	);

	always @(posedge HCLK or negedge HRESETn) if(~HRESETn) TXFIFOT_REG <= 0; else if(ahbl_we & (last_HADDR[15:0]==TXFIFOT_REG_ADDR)) TXFIFOT_REG <= HWDATA[4-1:0];
	always @(posedge HCLK or negedge HRESETn) if(~HRESETn) RXFIFOT_REG <= 0; else if(ahbl_we & (last_HADDR[15:0]==RXFIFOT_REG_ADDR)) RXFIFOT_REG <= HWDATA[4-1:0];
	always @(posedge HCLK or negedge HRESETn) if(~HRESETn) CONTROL_REG <= 0; else if(ahbl_we & (last_HADDR[15:0]==CONTROL_REG_ADDR)) CONTROL_REG <= HWDATA[1-1:0];
	always @(posedge HCLK or negedge HRESETn) if(~HRESETn) IM_REG <= 0; else if(ahbl_we & (last_HADDR[15:0]==IM_REG_ADDR)) IM_REG <= HWDATA[6-1:0];
	always @(posedge HCLK or negedge HRESETn) if(~HRESETn) CG_REG <= 0; else if(ahbl_we & (last_HADDR[15:0]==CG_REG_ADDR)) CG_REG <= HWDATA[1-1:0];

	always @(posedge HCLK or negedge HRESETn) if(~HRESETn) ICR_REG <= 6'b0; else if(ahbl_we & (last_HADDR[15:0]==ICR_REG_ADDR)) ICR_REG <= HWDATA[6-1:0]; else ICR_REG <= 6'd0;

	always @(posedge HCLK or negedge HRESETn)
		if(~HRESETn) RIS_REG <= 6'd0;
		else begin
			if(_TX_EMPTY_FLAG_FLAG_) RIS_REG[0] <= 1'b1; else if(ICR_REG[0]) RIS_REG[0] <= 1'b0;
			if(_TX_BELOW_FLAG_FLAG_) RIS_REG[1] <= 1'b1; else if(ICR_REG[1]) RIS_REG[1] <= 1'b0;
			if(_RX_FULL_FLAG_FLAG_) RIS_REG[2] <= 1'b1; else if(ICR_REG[2]) RIS_REG[2] <= 1'b0;
			if(_RX_ABOVE_FLAG_FLAG_) RIS_REG[3] <= 1'b1; else if(ICR_REG[3]) RIS_REG[3] <= 1'b0;
			if(_RX_EMPTY_FLAG_FLAG_) RIS_REG[4] <= 1'b1; else if(ICR_REG[4]) RIS_REG[4] <= 1'b0;
			if(_TX_FULL_FLAG_FLAG_) RIS_REG[5] <= 1'b1; else if(ICR_REG[5]) RIS_REG[5] <= 1'b0;

		end

	assign irq = |MIS_REG;

	assign	HRDATA = 
			(last_HADDR[15:0] == TXFIFOT_REG_ADDR) ? TXFIFOT_REG :
			(last_HADDR[15:0] == RXFIFOT_REG_ADDR) ? RXFIFOT_REG :
			(last_HADDR[15:0] == CONTROL_REG_ADDR) ? CONTROL_REG :
			(last_HADDR[15:0] == RIS_REG_ADDR) ? RIS_REG :
			(last_HADDR[15:0] == ICR_REG_ADDR) ? ICR_REG :
			(last_HADDR[15:0] == IM_REG_ADDR) ? IM_REG :
			(last_HADDR[15:0] == CG_REG_ADDR) ? CG_REG :
			(last_HADDR[15:0] == RXDATA_REG_ADDR) ? RXDATA_REG :
			(last_HADDR[15:0] == TXFIFOLEVEL_REG_ADDR) ? TXFIFOLEVEL_REG :
			(last_HADDR[15:0] == RXFIFOLEVEL_REG_ADDR) ? RXFIFOLEVEL_REG :
			(last_HADDR[15:0] == MIS_REG_ADDR) ? MIS_REG :
			32'hDEADBEEF;


	assign HREADYOUT = 1'b1;

endmodule

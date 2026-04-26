
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

`define		APB_BLOCK(name, init)		always @(posedge PCLK or negedge PRESETn) if(~PRESETn) name <= init;
`define		APB_REG(name, init, size)	`APB_BLOCK(name, init) else if(apb_we & (PADDR[15:0]==``name``_ADDR)) name <= PWDATA[``size``-1:0];
`define		APB_ICR(size)				`APB_BLOCK(ICR_REG, ``size``'b0) else if(apb_we & (PADDR[15:0]==ICR_REG_ADDR)) ICR_REG <= PWDATA[``size``-1:0]; else ICR_REG <= ``size``'d0;

module usb_cdc_wrapper_apb (
	output	wire 		dp_pu_o,
	input	wire 		dp_rx_i,
	input	wire 		dn_rx_i,
	output	wire 		dp_tx_o,
	output	wire 		dn_tx_o,
	output	wire 		tx_en_o,
	input	wire 		PCLK,
	input	wire		usb_cdc_clk_48MHz,
	input	wire 		PRESETn,
	input	wire [31:0]	PADDR,
	input	wire 		PWRITE,
	input	wire 		PSEL,
	input	wire 		PENABLE,
	input	wire [31:0]	PWDATA,
	output	wire [31:0]	PRDATA,
	output	wire 		PREADY,
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
	wire		apb_valid	= PSEL & PENABLE;
	wire		apb_we	= PWRITE & apb_valid;
	wire		apb_re	= ~PWRITE & apb_valid;
	wire		_clk_	= PCLK;
	wire		_gclk_;
	wire		_rst_	= ~PRESETn;
	wire		rx_fifo_rd	= (apb_re & (PADDR[15:0]==RXDATA_REG_ADDR));
	wire		tx_fifo_wr	= (apb_we & (PADDR[15:0]==TXDATA_REG_ADDR));
	wire[7:0]	tx_fifo_wdata	= PWDATA[7:0];

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

	`APB_REG(TXFIFOT_REG, 0, 4)
	`APB_REG(RXFIFOT_REG, 0, 4)
	`APB_REG(CONTROL_REG, 0, 1)
	`APB_REG(IM_REG, 0, 6)
	`APB_REG(CG_REG, 0, 1)

	`APB_ICR(6)

	always @(posedge PCLK or negedge PRESETn)
		if(~PRESETn) RIS_REG <= 6'd0;
		else begin
			if(_TX_EMPTY_FLAG_FLAG_) RIS_REG[0] <= 1'b1; else if(ICR_REG[0]) RIS_REG[0] <= 1'b0;
			if(_TX_BELOW_FLAG_FLAG_) RIS_REG[1] <= 1'b1; else if(ICR_REG[1]) RIS_REG[1] <= 1'b0;
			if(_RX_FULL_FLAG_FLAG_) RIS_REG[2] <= 1'b1; else if(ICR_REG[2]) RIS_REG[2] <= 1'b0;
			if(_RX_ABOVE_FLAG_FLAG_) RIS_REG[3] <= 1'b1; else if(ICR_REG[3]) RIS_REG[3] <= 1'b0;
			if(_RX_EMPTY_FLAG_FLAG_) RIS_REG[4] <= 1'b1; else if(ICR_REG[4]) RIS_REG[4] <= 1'b0;
			if(_TX_FULL_FLAG_FLAG_) RIS_REG[5] <= 1'b1; else if(ICR_REG[5]) RIS_REG[5] <= 1'b0;

		end

	assign irq = |MIS_REG;

	assign	PRDATA = 
			(PADDR[15:0] == TXFIFOT_REG_ADDR) ? TXFIFOT_REG :
			(PADDR[15:0] == RXFIFOT_REG_ADDR) ? RXFIFOT_REG :
			(PADDR[15:0] == CONTROL_REG_ADDR) ? CONTROL_REG :
			(PADDR[15:0] == RIS_REG_ADDR) ? RIS_REG :
			(PADDR[15:0] == ICR_REG_ADDR) ? ICR_REG :
			(PADDR[15:0] == IM_REG_ADDR) ? IM_REG :
			(PADDR[15:0] == CG_REG_ADDR) ? CG_REG :
			(PADDR[15:0] == RXDATA_REG_ADDR) ? RXDATA_REG :
			(PADDR[15:0] == TXFIFOLEVEL_REG_ADDR) ? TXFIFOLEVEL_REG :
			(PADDR[15:0] == RXFIFOLEVEL_REG_ADDR) ? RXFIFOLEVEL_REG :
			(PADDR[15:0] == MIS_REG_ADDR) ? MIS_REG :
			32'hDEADBEEF;


	assign PREADY = 1'b1;

endmodule

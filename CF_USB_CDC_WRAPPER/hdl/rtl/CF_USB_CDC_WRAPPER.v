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

module usb_cdc_wrapper (

    input wire              clk,
    input wire              usb_cdc_clk_48MHz,
    input wire              rst_n,

    input wire              rx_fifo_rd,
    output wire             rx_fifo_full,
    output wire             rx_fifo_empty,
    output wire [3:0]       rx_fifo_level,
    output wire [7:0]       rx_fifo_rdata,
    input  wire [3:0]       rx_fifo_th,
    output wire             rx_fifo_level_above,


    input wire              tx_fifo_wr,
    output wire             tx_fifo_full,
    output wire             tx_fifo_empty,
    output wire [3:0]       tx_fifo_level,
    input wire [7:0]        tx_fifo_wdata,
    input  wire [3:0]       tx_fifo_th,
    output wire             tx_fifo_level_below,

    output  wire            dp_pu_o,
    input   wire            dp_rx_i,
    input   wire            dn_rx_i,
    output  wire            dp_tx_o,
    output  wire            dn_tx_o,
    output  wire            tx_en_o

);

    wire [7:0]       out_data_o;
    wire             out_valid_o;
    wire             out_ready_i;

    wire [7:0]       in_data_i;
    wire             in_valid_i;
    wire             in_ready_o;
       
        
    assign out_ready_i = ~rx_fifo_full;
    assign rx_fifo_level_above = (rx_fifo_level > rx_fifo_th);


    assign in_valid_i = ~tx_fifo_empty;
    assign tx_fifo_level_below = (tx_fifo_level < tx_fifo_th);
    wire tx_fifo_read = in_ready_o & ~tx_fifo_empty;
    
    localparam BIT_SAMPLES = 'd4;
    localparam [6:0] DIVF = 12*BIT_SAMPLES-1;
    
    usb_cdc #(.VENDORID(16'h1D50),
             .PRODUCTID(16'h6130),
             .IN_BULK_MAXPACKETSIZE('d8),
             .OUT_BULK_MAXPACKETSIZE('d8),
             .BIT_SAMPLES(BIT_SAMPLES),
             .USE_APP_CLK(1),
             .APP_CLK_RATIO(2))  // 48/24 MHz
   u_usb_cdc (.frame_o(),
              .configured_o(),
              .app_clk_i(clk), // 24 MHz
              .clk_i(usb_cdc_clk_48MHz), //48 MHz
              .rstn_i(rst_n),
              .out_ready_i(out_ready_i),
              .in_data_i(in_data_i),
              .in_valid_i(in_valid_i),
              .dp_rx_i(dp_rx_i),
              .dn_rx_i(dn_rx_i),
              .out_data_o(out_data_o),
              .out_valid_o(out_valid_o),
              .in_ready_o(in_ready_o),
              .dp_pu_o(dp_pu_o),
              .tx_en_o(tx_en_o),
              .dp_tx_o(dp_tx_o),
              .dn_tx_o(dn_tx_o));

    USB_CDC_FIFO rx_fifo (
        .clk(clk),
        .rst_n(rst_n),
        .rd(rx_fifo_rd),
        .wr(out_valid_o),  
        .w_data(out_data_o),  //data recieved from usb cdc 
        .empty(rx_fifo_empty),
        .full(rx_fifo_full),
        .r_data(rx_fifo_rdata), //data going to hrx_fifo_rdata
        .level(rx_fifo_level)
    );


    USB_CDC_FIFO tx_fifo (
        .clk(clk),
        .rst_n(rst_n),
        .rd(tx_fifo_read),
        .wr(tx_fifo_wr),
        .w_data(tx_fifo_wdata), //data coming from ptx_fifo_wdata going to usb to transmit it 
        .empty(tx_fifo_empty),
        .full(tx_fifo_full),
        .r_data(in_data_i),  //data going to usb cdc
        .level(tx_fifo_level)
    );


endmodule


module USB_CDC_FIFO #(parameter DW=8, AW=4)(
    input     wire            clk,
    input     wire            rst_n,
    input     wire            rd,
    input     wire            wr,
    input     wire [DW-1:0]   w_data,
    output    wire            empty,
    output    wire            full,
    output    wire [DW-1:0]   r_data,
    output    wire [AW-1:0]   level    
);

    localparam  DEPTH = 2**AW;

    //Internal Signal declarations
    reg [DW-1:0]  array_reg [DEPTH-1:0];
    reg [AW-1:0]  w_ptr_reg;
    reg [AW-1:0]  w_ptr_next;
    reg [AW-1:0]  w_ptr_succ;
    reg [AW-1:0]  r_ptr_reg;
    reg [AW-1:0]  r_ptr_next;
    reg [AW-1:0]  r_ptr_succ;

  // Level
    reg [AW-1:0] level_reg;
    reg [AW-1:0] level_next;      
    reg full_reg;
    reg empty_reg;
    reg full_next;
    reg empty_next;
  
  wire w_en;
  

  always @ (posedge clk)
    if(w_en)
    begin
      array_reg[w_ptr_reg] <= w_data;
    end

  assign r_data = array_reg[r_ptr_reg];   

  assign w_en = wr & ~full_reg;           

//State Machine
  always @ (posedge clk, negedge rst_n)
  begin
    if(!rst_n)
      begin
        w_ptr_reg <= 0;
        r_ptr_reg <= 0;
        full_reg <= 1'b0;
        empty_reg <= 1'b1;
        level_reg <= 4'd0;
      end
    else
      begin
        w_ptr_reg <= w_ptr_next;
        r_ptr_reg <= r_ptr_next;
        full_reg <= full_next;
        empty_reg <= empty_next;
        level_reg <= level_next;
      end
  end


//Next State Logic
  always @*
  begin
    w_ptr_succ = w_ptr_reg + 1;
    r_ptr_succ = r_ptr_reg + 1;
    
    w_ptr_next = w_ptr_reg;
    r_ptr_next = r_ptr_reg;
    full_next = full_reg;
    empty_next = empty_reg;
    level_next = level_reg;
    
    case({w_en,rd})
      //2'b00: nop
      2'b01:
        if(~empty_reg)
          begin
            r_ptr_next = r_ptr_succ;
            full_next = 1'b0;
            level_next = level_reg - 1;
            if (r_ptr_succ == w_ptr_reg)
              empty_next = 1'b1;
          end
      2'b10:
        if(~full_reg)
          begin
            w_ptr_next = w_ptr_succ;
            empty_next = 1'b0;
            level_next = level_reg + 1;
            if (w_ptr_succ == r_ptr_reg)
              full_next = 1'b1;
          end
      2'b11:
        begin
          w_ptr_next = w_ptr_succ;
          r_ptr_next = r_ptr_succ;
        end
    endcase
  end

    //Set Full and Empty

  assign full = full_reg;
  assign empty = empty_reg;

  assign level = level_reg;
  
endmodule
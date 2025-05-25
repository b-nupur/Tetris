module Domand(
    clk,
    a0,
    a1,
    a2,
    b0,
    b1,
    b2,
    r01,
    r02,
    r12,
    dec_0,
    c0,
    c1,
    c2,
);
//INPUTS
    input clk;
    input  [7:0] a0;
    input  [7:0] a1;
    input  [7:0] a2;
    input  [7:0] b0;
    input  [7:0] b1;
    input  [7:0] b2;
    input  [7:0] r01;
    input  [7:0] r02;
    input  [7:0] r12;
    input  [7:0] dec_0;
//OUTPUTS
    output reg  [7:0] c0;
    output reg  [7:0] c1;
    output reg  [7:0] c2;
//Intermediate values
    wire [7:0] dec_0_inp;
    reg [7:0] z1_assgn1;
    wire [7:0] a0_inp;
    wire [7:0] a1_inp;
    wire [7:0] a2_inp;
    wire [7:0] b0_inp;
    wire [7:0] b1_inp;
    wire [7:0] b2_inp;
    wire [7:0] r01_inp;
    wire [7:0] r02_inp;
    wire [7:0] r12_inp;
    wire [7:0] t0;
    wire [7:0] t1;
    wire [7:0] i0;
    wire [7:0] t2;
    wire [7:0] i1;
    wire [7:0] t3;
    wire [7:0] i2;
    wire [7:0] t4;
    wire [7:0] t5;
    wire [7:0] i3;
    wire [7:0] t6;
    wire [7:0] i4;
    wire [7:0] t7;
    wire [7:0] i5;
    wire [7:0] t8;
    wire [7:0] t9;
    reg [7:0] i0_reg;
    reg [7:0] i1_reg;
    reg [7:0] t0_reg;
    wire [7:0] t10;
    reg [7:0] i2_reg;
    reg [7:0] i3_reg;
    reg [7:0] t4_reg;
    wire [7:0] t11;
    reg [7:0] i4_reg;
    reg [7:0] i5_reg;
    reg [7:0] t8_reg;

    assign dec_0_inp = dec_0;
    assign a0_inp = a0;
    assign a1_inp = a1;
    assign a2_inp = a2;
    assign b0_inp = b0;
    assign b1_inp = b1;
    assign b2_inp = b2;
    assign r01_inp = r01;
    assign r02_inp = r02;
    assign r12_inp = r12;
    assign t0 = (a0_inp & b0_inp);
    assign t1 = (a0_inp & b1_inp);
    assign i0 = (t1 ^ r01_inp);
    assign t2 = (a0_inp & b2_inp);
    assign i1 = (t2 ^ r02_inp);
    assign t3 = (a1_inp & b0_inp);
    assign i2 = (t3 ^ r01_inp);
    assign t4 = (a1_inp & b1_inp);
    assign t5 = (a1_inp & b2_inp);
    assign i3 = (t5 ^ r12_inp);
    assign t6 = (a2_inp & b0_inp);
    assign i4 = (t6 ^ r02_inp);
    assign t7 = (a2_inp & b1_inp);
    assign i5 = (t7 ^ r12_inp);
    assign t8 = (a2_inp & b2_inp);
    assign t9 = (i0_reg ^ i1_reg);
    assign t10 = (i2_reg ^ i3_reg);
    assign t11 = (i4_reg ^ i5_reg);

    always @(posedge clk) begin
        z1_assgn1 <= dec_0_inp;
        i0_reg <= i0;
        i1_reg <= i1;
        t0_reg <= t0;
        c0 <= (t9 ^ t0_reg);
        i2_reg <= i2;
        i3_reg <= i3;
        t4_reg <= t4;
        c1 <= (t10 ^ t4_reg);
        i4_reg <= i4;
        i5_reg <= i5;
        t8_reg <= t8;
        c2 <= (t11 ^ t8_reg);
    end

endmodule


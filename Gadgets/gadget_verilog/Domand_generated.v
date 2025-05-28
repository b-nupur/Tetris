module Domand(
    clk,
    a0,
    a1,
    a2,
    a3,
    a4,
    b0,
    b1,
    b2,
    b3,
    b4,
    r01,
    r02,
    r03,
    r04,
    r12,
    r13,
    r14,
    r23,
    r24,
    r34,
    dec_0,
    c0,
    c1,
    c2,
    c3,
    c4,
);
//INPUTS
    input clk;
    input  [7:0] a0;
    input  [7:0] a1;
    input  [7:0] a2;
    input  [7:0] a3;
    input  [7:0] a4;
    input  [7:0] b0;
    input  [7:0] b1;
    input  [7:0] b2;
    input  [7:0] b3;
    input  [7:0] b4;
    input  [7:0] r01;
    input  [7:0] r02;
    input  [7:0] r03;
    input  [7:0] r04;
    input  [7:0] r12;
    input  [7:0] r13;
    input  [7:0] r14;
    input  [7:0] r23;
    input  [7:0] r24;
    input  [7:0] r34;
    input  [7:0] dec_0;
//OUTPUTS
    output reg  [7:0] c0;
    output reg  [7:0] c1;
    output reg  [7:0] c2;
    output reg  [7:0] c3;
    output reg  [7:0] c4;
//Intermediate values
    wire [7:0] dec_0_inp;
    reg [7:0] z1_assgn1;
    wire [7:0] a0_inp;
    wire [7:0] a1_inp;
    wire [7:0] a2_inp;
    wire [7:0] a3_inp;
    wire [7:0] a4_inp;
    wire [7:0] b0_inp;
    wire [7:0] b1_inp;
    wire [7:0] b2_inp;
    wire [7:0] b3_inp;
    wire [7:0] b4_inp;
    wire [7:0] r01_inp;
    wire [7:0] r02_inp;
    wire [7:0] r03_inp;
    wire [7:0] r04_inp;
    wire [7:0] r12_inp;
    wire [7:0] r13_inp;
    wire [7:0] r14_inp;
    wire [7:0] r23_inp;
    wire [7:0] r24_inp;
    wire [7:0] r34_inp;
    wire [7:0] t0;
    wire [7:0] t1;
    wire [7:0] i0;
    wire [7:0] t2;
    wire [7:0] i1;
    wire [7:0] t3;
    wire [7:0] i2;
    wire [7:0] t4;
    wire [7:0] i3;
    wire [7:0] t5;
    wire [7:0] i4;
    wire [7:0] t6;
    wire [7:0] t7;
    wire [7:0] i5;
    wire [7:0] t8;
    wire [7:0] i6;
    wire [7:0] t9;
    wire [7:0] i7;
    wire [7:0] t10;
    wire [7:0] i8;
    wire [7:0] t11;
    wire [7:0] i9;
    wire [7:0] t12;
    wire [7:0] t13;
    wire [7:0] i10;
    wire [7:0] t14;
    wire [7:0] i11;
    wire [7:0] t15;
    wire [7:0] i12;
    wire [7:0] t16;
    wire [7:0] i13;
    wire [7:0] t17;
    wire [7:0] i14;
    wire [7:0] t18;
    wire [7:0] t19;
    wire [7:0] i15;
    wire [7:0] t20;
    wire [7:0] i16;
    wire [7:0] t21;
    wire [7:0] i17;
    wire [7:0] t22;
    wire [7:0] i18;
    wire [7:0] t23;
    wire [7:0] i19;
    wire [7:0] t24;
    wire [7:0] t25;
    reg [7:0] i0_reg;
    reg [7:0] i1_reg;
    wire [7:0] t26;
    reg [7:0] i2_reg;
    reg [7:0] i3_reg;
    reg [7:0] t0_reg;
    reg [7:0] i4_reg;
    reg [7:0] i5_reg;
    wire [7:0] t27;
    reg [7:0] i6_reg;
    reg [7:0] i7_reg;
    reg [7:0] t6_reg;
    reg [7:0] i8_reg;
    reg [7:0] i9_reg;
    wire [7:0] t28;
    reg [7:0] i10_reg;
    reg [7:0] i11_reg;
    reg [7:0] t12_reg;
    reg [7:0] i12_reg;
    reg [7:0] i13_reg;
    wire [7:0] t29;
    reg [7:0] i14_reg;
    reg [7:0] i15_reg;
    reg [7:0] t18_reg;
    reg [7:0] i16_reg;
    reg [7:0] i17_reg;
    wire [7:0] t30;
    reg [7:0] i18_reg;
    reg [7:0] i19_reg;
    reg [7:0] t24_reg;

    assign dec_0_inp = dec_0;
    assign a0_inp = a0;
    assign a1_inp = a1;
    assign a2_inp = a2;
    assign a3_inp = a3;
    assign a4_inp = a4;
    assign b0_inp = b0;
    assign b1_inp = b1;
    assign b2_inp = b2;
    assign b3_inp = b3;
    assign b4_inp = b4;
    assign r01_inp = r01;
    assign r02_inp = r02;
    assign r03_inp = r03;
    assign r04_inp = r04;
    assign r12_inp = r12;
    assign r13_inp = r13;
    assign r14_inp = r14;
    assign r23_inp = r23;
    assign r24_inp = r24;
    assign r34_inp = r34;
    assign t0 = (a0_inp & b0_inp);
    assign t1 = (a0_inp & b1_inp);
    assign i0 = (t1 ^ r01_inp);
    assign t2 = (a0_inp & b2_inp);
    assign i1 = (t2 ^ r02_inp);
    assign t3 = (a0_inp & b3_inp);
    assign i2 = (t3 ^ r03_inp);
    assign t4 = (a0_inp & b4_inp);
    assign i3 = (t4 ^ r04_inp);
    assign t5 = (a1_inp & b0_inp);
    assign i4 = (t5 ^ r01_inp);
    assign t6 = (a1_inp & b1_inp);
    assign t7 = (a1_inp & b2_inp);
    assign i5 = (t7 ^ r12_inp);
    assign t8 = (a1_inp & b3_inp);
    assign i6 = (t8 ^ r13_inp);
    assign t9 = (a1_inp & b4_inp);
    assign i7 = (t9 ^ r14_inp);
    assign t10 = (a2_inp & b0_inp);
    assign i8 = (t10 ^ r02_inp);
    assign t11 = (a2_inp & b1_inp);
    assign i9 = (t11 ^ r12_inp);
    assign t12 = (a2_inp & b2_inp);
    assign t13 = (a2_inp & b3_inp);
    assign i10 = (t13 ^ r23_inp);
    assign t14 = (a2_inp & b4_inp);
    assign i11 = (t14 ^ r24_inp);
    assign t15 = (a3_inp & b0_inp);
    assign i12 = (t15 ^ r03_inp);
    assign t16 = (a3_inp & b1_inp);
    assign i13 = (t16 ^ r13_inp);
    assign t17 = (a3_inp & b2_inp);
    assign i14 = (t17 ^ r23_inp);
    assign t18 = (a3_inp & b3_inp);
    assign t19 = (a3_inp & b4_inp);
    assign i15 = (t19 ^ r34_inp);
    assign t20 = (a4_inp & b0_inp);
    assign i16 = (t20 ^ r04_inp);
    assign t21 = (a4_inp & b1_inp);
    assign i17 = (t21 ^ r14_inp);
    assign t22 = (a4_inp & b2_inp);
    assign i18 = (t22 ^ r24_inp);
    assign t23 = (a4_inp & b3_inp);
    assign i19 = (t23 ^ r34_inp);
    assign t24 = (a4_inp & b4_inp);
    assign t25 = (i0_reg ^ i1_reg);
    assign t26 = (i4_reg ^ i5_reg);
    assign t27 = (i8_reg ^ i9_reg);
    assign t28 = (i12_reg ^ i13_reg);
    assign t29 = (i16_reg ^ i17_reg);
    assign t30 = (t29 ^ i19_reg);

    always @(posedge clk) begin
        z1_assgn1 <= dec_0_inp;
        i0_reg <= i0;
        i1_reg <= i1;
        i2_reg <= i2;
        i3_reg <= i3;
        t0_reg <= t0;
        c0 <= (t25 ^ t0_reg);
        i4_reg <= i4;
        i5_reg <= i5;
        i6_reg <= i6;
        i7_reg <= i7;
        t6_reg <= t6;
        c1 <= (t26 ^ t6_reg);
        i8_reg <= i8;
        i9_reg <= i9;
        i10_reg <= i10;
        i11_reg <= i11;
        t12_reg <= t12;
        c2 <= (t27 ^ t12_reg);
        i12_reg <= i12;
        i13_reg <= i13;
        i14_reg <= i14;
        i15_reg <= i15;
        t18_reg <= t18;
        c3 <= (t28 ^ t18_reg);
        i16_reg <= i16;
        i17_reg <= i17;
        i18_reg <= i18;
        i19_reg <= i19;
        t24_reg <= t24;
        c4 <= (t29 ^ t24_reg);
    end

endmodule


module HPC3(
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
    p01,
    p02,
    p03,
    p04,
    p12,
    p13,
    p14,
    p23,
    p24,
    p34,
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
    input  [7:0] p01;
    input  [7:0] p02;
    input  [7:0] p03;
    input  [7:0] p04;
    input  [7:0] p12;
    input  [7:0] p13;
    input  [7:0] p14;
    input  [7:0] p23;
    input  [7:0] p24;
    input  [7:0] p34;
//OUTPUTS
    output reg  [7:0] c0;
    output reg  [7:0] c1;
    output reg  [7:0] c2;
    output reg  [7:0] c3;
    output reg  [7:0] c4;
//Intermediate values
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
    wire [7:0] p01_inp;
    wire [7:0] p02_inp;
    wire [7:0] p03_inp;
    wire [7:0] p04_inp;
    wire [7:0] p12_inp;
    wire [7:0] p13_inp;
    wire [7:0] p14_inp;
    wire [7:0] p23_inp;
    wire [7:0] p24_inp;
    wire [7:0] p34_inp;
    reg [7:0] u00;
    reg [7:0] temp_hpc3_v_4_order0;
    reg [7:0] a_share_reg_hpc3_v_4_order0;
    wire [7:0] v01;
    wire [7:0] a_share_neg_hpc3_w_4_order0;
    wire [7:0] temp_hpc3_w_4_order0;
    reg [7:0] w01;
    wire [7:0] u01;
    reg [7:0] temp_hpc3_v_4_order1;
    reg [7:0] a_share_reg_hpc3_v_4_order1;
    wire [7:0] v02;
    wire [7:0] a_share_neg_hpc3_w_4_order1;
    wire [7:0] temp_hpc3_w_4_order1;
    reg [7:0] w02;
    wire [7:0] u02;
    reg [7:0] temp_hpc3_v_4_order2;
    reg [7:0] a_share_reg_hpc3_v_4_order2;
    wire [7:0] v03;
    wire [7:0] a_share_neg_hpc3_w_4_order2;
    wire [7:0] temp_hpc3_w_4_order2;
    reg [7:0] w03;
    wire [7:0] u03;
    reg [7:0] temp_hpc3_v_4_order3;
    reg [7:0] a_share_reg_hpc3_v_4_order3;
    wire [7:0] v04;
    wire [7:0] a_share_neg_hpc3_w_4_order3;
    wire [7:0] temp_hpc3_w_4_order3;
    reg [7:0] w04;
    wire [7:0] u04;
    reg [7:0] temp_hpc3_v_4_order4;
    reg [7:0] a_share_reg_hpc3_v_4_order4;
    wire [7:0] v10;
    wire [7:0] a_share_neg_hpc3_w_4_order4;
    wire [7:0] temp_hpc3_w_4_order4;
    reg [7:0] w10;
    wire [7:0] u10;
    reg [7:0] u11;
    reg [7:0] temp_hpc3_v_4_order5;
    reg [7:0] a_share_reg_hpc3_v_4_order5;
    wire [7:0] v12;
    wire [7:0] a_share_neg_hpc3_w_4_order5;
    wire [7:0] temp_hpc3_w_4_order5;
    reg [7:0] w12;
    wire [7:0] u12;
    reg [7:0] temp_hpc3_v_4_order6;
    reg [7:0] a_share_reg_hpc3_v_4_order6;
    wire [7:0] v13;
    wire [7:0] a_share_neg_hpc3_w_4_order6;
    wire [7:0] temp_hpc3_w_4_order6;
    reg [7:0] w13;
    wire [7:0] u13;
    reg [7:0] temp_hpc3_v_4_order7;
    reg [7:0] a_share_reg_hpc3_v_4_order7;
    wire [7:0] v14;
    wire [7:0] a_share_neg_hpc3_w_4_order7;
    wire [7:0] temp_hpc3_w_4_order7;
    reg [7:0] w14;
    wire [7:0] u14;
    reg [7:0] temp_hpc3_v_4_order8;
    reg [7:0] a_share_reg_hpc3_v_4_order8;
    wire [7:0] v20;
    wire [7:0] a_share_neg_hpc3_w_4_order8;
    wire [7:0] temp_hpc3_w_4_order8;
    reg [7:0] w20;
    wire [7:0] u20;
    reg [7:0] temp_hpc3_v_4_order9;
    reg [7:0] a_share_reg_hpc3_v_4_order9;
    wire [7:0] v21;
    wire [7:0] a_share_neg_hpc3_w_4_order9;
    wire [7:0] temp_hpc3_w_4_order9;
    reg [7:0] w21;
    wire [7:0] u21;
    reg [7:0] u22;
    reg [7:0] temp_hpc3_v_4_order10;
    reg [7:0] a_share_reg_hpc3_v_4_order10;
    wire [7:0] v23;
    wire [7:0] a_share_neg_hpc3_w_4_order10;
    wire [7:0] temp_hpc3_w_4_order10;
    reg [7:0] w23;
    wire [7:0] u23;
    reg [7:0] temp_hpc3_v_4_order11;
    reg [7:0] a_share_reg_hpc3_v_4_order11;
    wire [7:0] v24;
    wire [7:0] a_share_neg_hpc3_w_4_order11;
    wire [7:0] temp_hpc3_w_4_order11;
    reg [7:0] w24;
    wire [7:0] u24;
    reg [7:0] temp_hpc3_v_4_order12;
    reg [7:0] a_share_reg_hpc3_v_4_order12;
    wire [7:0] v30;
    wire [7:0] a_share_neg_hpc3_w_4_order12;
    wire [7:0] temp_hpc3_w_4_order12;
    reg [7:0] w30;
    wire [7:0] u30;
    reg [7:0] temp_hpc3_v_4_order13;
    reg [7:0] a_share_reg_hpc3_v_4_order13;
    wire [7:0] v31;
    wire [7:0] a_share_neg_hpc3_w_4_order13;
    wire [7:0] temp_hpc3_w_4_order13;
    reg [7:0] w31;
    wire [7:0] u31;
    reg [7:0] temp_hpc3_v_4_order14;
    reg [7:0] a_share_reg_hpc3_v_4_order14;
    wire [7:0] v32;
    wire [7:0] a_share_neg_hpc3_w_4_order14;
    wire [7:0] temp_hpc3_w_4_order14;
    reg [7:0] w32;
    wire [7:0] u32;
    reg [7:0] u33;
    reg [7:0] temp_hpc3_v_4_order15;
    reg [7:0] a_share_reg_hpc3_v_4_order15;
    wire [7:0] v34;
    wire [7:0] a_share_neg_hpc3_w_4_order15;
    wire [7:0] temp_hpc3_w_4_order15;
    reg [7:0] w34;
    wire [7:0] u34;
    reg [7:0] temp_hpc3_v_4_order16;
    reg [7:0] a_share_reg_hpc3_v_4_order16;
    wire [7:0] v40;
    wire [7:0] a_share_neg_hpc3_w_4_order16;
    wire [7:0] temp_hpc3_w_4_order16;
    reg [7:0] w40;
    wire [7:0] u40;
    reg [7:0] temp_hpc3_v_4_order17;
    reg [7:0] a_share_reg_hpc3_v_4_order17;
    wire [7:0] v41;
    wire [7:0] a_share_neg_hpc3_w_4_order17;
    wire [7:0] temp_hpc3_w_4_order17;
    reg [7:0] w41;
    wire [7:0] u41;
    reg [7:0] temp_hpc3_v_4_order18;
    reg [7:0] a_share_reg_hpc3_v_4_order18;
    wire [7:0] v42;
    wire [7:0] a_share_neg_hpc3_w_4_order18;
    wire [7:0] temp_hpc3_w_4_order18;
    reg [7:0] w42;
    wire [7:0] u42;
    reg [7:0] temp_hpc3_v_4_order19;
    reg [7:0] a_share_reg_hpc3_v_4_order19;
    wire [7:0] v43;
    wire [7:0] a_share_neg_hpc3_w_4_order19;
    wire [7:0] temp_hpc3_w_4_order19;
    reg [7:0] w43;
    wire [7:0] u43;
    reg [7:0] u44;
    wire [7:0] t1;
    wire [7:0] t2;
    wire [7:0] t3;
    wire [7:0] t4;
    wire [7:0] t5;
    wire [7:0] t6;
    wire [7:0] t7;
    wire [7:0] t8;
    wire [7:0] t9;
    wire [7:0] t10;
    wire [7:0] t11;
    wire [7:0] t12;
    wire [7:0] t13;
    wire [7:0] t14;
    wire [7:0] t15;

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
    assign p01_inp = p01;
    assign p02_inp = p02;
    assign p03_inp = p03;
    assign p04_inp = p04;
    assign p12_inp = p12;
    assign p13_inp = p13;
    assign p14_inp = p14;
    assign p23_inp = p23;
    assign p24_inp = p24;
    assign p34_inp = p34;
    assign v01 = (temp_hpc3_v_4_order0 & a_share_reg_hpc3_v_4_order0);
    assign a_share_neg_hpc3_w_4_order0 = !a0_inp;
    assign temp_hpc3_w_4_order0 = (a_share_neg_hpc3_w_4_order0 & r01_inp);
    assign u01 = (v01 ^ w01);
    assign v02 = (temp_hpc3_v_4_order1 & a_share_reg_hpc3_v_4_order1);
    assign a_share_neg_hpc3_w_4_order1 = !a0_inp;
    assign temp_hpc3_w_4_order1 = (a_share_neg_hpc3_w_4_order1 & r02_inp);
    assign u02 = (v02 ^ w02);
    assign v03 = (temp_hpc3_v_4_order2 & a_share_reg_hpc3_v_4_order2);
    assign a_share_neg_hpc3_w_4_order2 = !a0_inp;
    assign temp_hpc3_w_4_order2 = (a_share_neg_hpc3_w_4_order2 & r03_inp);
    assign u03 = (v03 ^ w03);
    assign v04 = (temp_hpc3_v_4_order3 & a_share_reg_hpc3_v_4_order3);
    assign a_share_neg_hpc3_w_4_order3 = !a0_inp;
    assign temp_hpc3_w_4_order3 = (a_share_neg_hpc3_w_4_order3 & r04_inp);
    assign u04 = (v04 ^ w04);
    assign v10 = (temp_hpc3_v_4_order4 & a_share_reg_hpc3_v_4_order4);
    assign a_share_neg_hpc3_w_4_order4 = !a1_inp;
    assign temp_hpc3_w_4_order4 = (a_share_neg_hpc3_w_4_order4 & r01_inp);
    assign u10 = (v10 ^ w10);
    assign v12 = (temp_hpc3_v_4_order5 & a_share_reg_hpc3_v_4_order5);
    assign a_share_neg_hpc3_w_4_order5 = !a1_inp;
    assign temp_hpc3_w_4_order5 = (a_share_neg_hpc3_w_4_order5 & r12_inp);
    assign u12 = (v12 ^ w12);
    assign v13 = (temp_hpc3_v_4_order6 & a_share_reg_hpc3_v_4_order6);
    assign a_share_neg_hpc3_w_4_order6 = !a1_inp;
    assign temp_hpc3_w_4_order6 = (a_share_neg_hpc3_w_4_order6 & r13_inp);
    assign u13 = (v13 ^ w13);
    assign v14 = (temp_hpc3_v_4_order7 & a_share_reg_hpc3_v_4_order7);
    assign a_share_neg_hpc3_w_4_order7 = !a1_inp;
    assign temp_hpc3_w_4_order7 = (a_share_neg_hpc3_w_4_order7 & r14_inp);
    assign u14 = (v14 ^ w14);
    assign v20 = (temp_hpc3_v_4_order8 & a_share_reg_hpc3_v_4_order8);
    assign a_share_neg_hpc3_w_4_order8 = !a2_inp;
    assign temp_hpc3_w_4_order8 = (a_share_neg_hpc3_w_4_order8 & r02_inp);
    assign u20 = (v20 ^ w20);
    assign v21 = (temp_hpc3_v_4_order9 & a_share_reg_hpc3_v_4_order9);
    assign a_share_neg_hpc3_w_4_order9 = !a2_inp;
    assign temp_hpc3_w_4_order9 = (a_share_neg_hpc3_w_4_order9 & r12_inp);
    assign u21 = (v21 ^ w21);
    assign v23 = (temp_hpc3_v_4_order10 & a_share_reg_hpc3_v_4_order10);
    assign a_share_neg_hpc3_w_4_order10 = !a2_inp;
    assign temp_hpc3_w_4_order10 = (a_share_neg_hpc3_w_4_order10 & r23_inp);
    assign u23 = (v23 ^ w23);
    assign v24 = (temp_hpc3_v_4_order11 & a_share_reg_hpc3_v_4_order11);
    assign a_share_neg_hpc3_w_4_order11 = !a2_inp;
    assign temp_hpc3_w_4_order11 = (a_share_neg_hpc3_w_4_order11 & r24_inp);
    assign u24 = (v24 ^ w24);
    assign v30 = (temp_hpc3_v_4_order12 & a_share_reg_hpc3_v_4_order12);
    assign a_share_neg_hpc3_w_4_order12 = !a3_inp;
    assign temp_hpc3_w_4_order12 = (a_share_neg_hpc3_w_4_order12 & r03_inp);
    assign u30 = (v30 ^ w30);
    assign v31 = (temp_hpc3_v_4_order13 & a_share_reg_hpc3_v_4_order13);
    assign a_share_neg_hpc3_w_4_order13 = !a3_inp;
    assign temp_hpc3_w_4_order13 = (a_share_neg_hpc3_w_4_order13 & r13_inp);
    assign u31 = (v31 ^ w31);
    assign v32 = (temp_hpc3_v_4_order14 & a_share_reg_hpc3_v_4_order14);
    assign a_share_neg_hpc3_w_4_order14 = !a3_inp;
    assign temp_hpc3_w_4_order14 = (a_share_neg_hpc3_w_4_order14 & r23_inp);
    assign u32 = (v32 ^ w32);
    assign v34 = (temp_hpc3_v_4_order15 & a_share_reg_hpc3_v_4_order15);
    assign a_share_neg_hpc3_w_4_order15 = !a3_inp;
    assign temp_hpc3_w_4_order15 = (a_share_neg_hpc3_w_4_order15 & r34_inp);
    assign u34 = (v34 ^ w34);
    assign v40 = (temp_hpc3_v_4_order16 & a_share_reg_hpc3_v_4_order16);
    assign a_share_neg_hpc3_w_4_order16 = !a4_inp;
    assign temp_hpc3_w_4_order16 = (a_share_neg_hpc3_w_4_order16 & r04_inp);
    assign u40 = (v40 ^ w40);
    assign v41 = (temp_hpc3_v_4_order17 & a_share_reg_hpc3_v_4_order17);
    assign a_share_neg_hpc3_w_4_order17 = !a4_inp;
    assign temp_hpc3_w_4_order17 = (a_share_neg_hpc3_w_4_order17 & r14_inp);
    assign u41 = (v41 ^ w41);
    assign v42 = (temp_hpc3_v_4_order18 & a_share_reg_hpc3_v_4_order18);
    assign a_share_neg_hpc3_w_4_order18 = !a4_inp;
    assign temp_hpc3_w_4_order18 = (a_share_neg_hpc3_w_4_order18 & r24_inp);
    assign u42 = (v42 ^ w42);
    assign v43 = (temp_hpc3_v_4_order19 & a_share_reg_hpc3_v_4_order19);
    assign a_share_neg_hpc3_w_4_order19 = !a4_inp;
    assign temp_hpc3_w_4_order19 = (a_share_neg_hpc3_w_4_order19 & r34_inp);
    assign u43 = (v43 ^ w43);
    assign t1 = (u00 ^ u01);
    assign t2 = (t1 ^ u02);
    assign t3 = (t2 ^ u03);
    assign t4 = (u10 ^ u11);
    assign t5 = (t4 ^ u12);
    assign t6 = (t5 ^ u13);
    assign t7 = (u20 ^ u21);
    assign t8 = (t7 ^ u22);
    assign t9 = (t8 ^ u23);
    assign t10 = (u30 ^ u31);
    assign t11 = (t10 ^ u32);
    assign t12 = (t11 ^ u33);
    assign t13 = (u40 ^ u41);
    assign t14 = (t13 ^ u42);
    assign t15 = (t14 ^ u43);

    always @(posedge clk) begin
        u00 <= (a0_inp & b0_inp);
        temp_hpc3_v_4_order0 <= (b1_inp ^ r01_inp);
        a_share_reg_hpc3_v_4_order0 <= a0_inp;
        w01 <= (temp_hpc3_w_4_order0 ^ p01_inp);
        temp_hpc3_v_4_order1 <= (b2_inp ^ r02_inp);
        a_share_reg_hpc3_v_4_order1 <= a0_inp;
        w02 <= (temp_hpc3_w_4_order1 ^ p02_inp);
        temp_hpc3_v_4_order2 <= (b3_inp ^ r03_inp);
        a_share_reg_hpc3_v_4_order2 <= a0_inp;
        w03 <= (temp_hpc3_w_4_order2 ^ p03_inp);
        temp_hpc3_v_4_order3 <= (b4_inp ^ r04_inp);
        a_share_reg_hpc3_v_4_order3 <= a0_inp;
        w04 <= (temp_hpc3_w_4_order3 ^ p04_inp);
        temp_hpc3_v_4_order4 <= (b0_inp ^ r01_inp);
        a_share_reg_hpc3_v_4_order4 <= a1_inp;
        w10 <= (temp_hpc3_w_4_order4 ^ p01_inp);
        u11 <= (a1_inp & b1_inp);
        temp_hpc3_v_4_order5 <= (b2_inp ^ r12_inp);
        a_share_reg_hpc3_v_4_order5 <= a1_inp;
        w12 <= (temp_hpc3_w_4_order5 ^ p12_inp);
        temp_hpc3_v_4_order6 <= (b3_inp ^ r13_inp);
        a_share_reg_hpc3_v_4_order6 <= a1_inp;
        w13 <= (temp_hpc3_w_4_order6 ^ p13_inp);
        temp_hpc3_v_4_order7 <= (b4_inp ^ r14_inp);
        a_share_reg_hpc3_v_4_order7 <= a1_inp;
        w14 <= (temp_hpc3_w_4_order7 ^ p14_inp);
        temp_hpc3_v_4_order8 <= (b0_inp ^ r02_inp);
        a_share_reg_hpc3_v_4_order8 <= a2_inp;
        w20 <= (temp_hpc3_w_4_order8 ^ p02_inp);
        temp_hpc3_v_4_order9 <= (b1_inp ^ r12_inp);
        a_share_reg_hpc3_v_4_order9 <= a2_inp;
        w21 <= (temp_hpc3_w_4_order9 ^ p12_inp);
        u22 <= (a2_inp & b2_inp);
        temp_hpc3_v_4_order10 <= (b3_inp ^ r23_inp);
        a_share_reg_hpc3_v_4_order10 <= a2_inp;
        w23 <= (temp_hpc3_w_4_order10 ^ p23_inp);
        temp_hpc3_v_4_order11 <= (b4_inp ^ r24_inp);
        a_share_reg_hpc3_v_4_order11 <= a2_inp;
        w24 <= (temp_hpc3_w_4_order11 ^ p24_inp);
        temp_hpc3_v_4_order12 <= (b0_inp ^ r03_inp);
        a_share_reg_hpc3_v_4_order12 <= a3_inp;
        w30 <= (temp_hpc3_w_4_order12 ^ p03_inp);
        temp_hpc3_v_4_order13 <= (b1_inp ^ r13_inp);
        a_share_reg_hpc3_v_4_order13 <= a3_inp;
        w31 <= (temp_hpc3_w_4_order13 ^ p13_inp);
        temp_hpc3_v_4_order14 <= (b2_inp ^ r23_inp);
        a_share_reg_hpc3_v_4_order14 <= a3_inp;
        w32 <= (temp_hpc3_w_4_order14 ^ p23_inp);
        u33 <= (a3_inp & b3_inp);
        temp_hpc3_v_4_order15 <= (b4_inp ^ r34_inp);
        a_share_reg_hpc3_v_4_order15 <= a3_inp;
        w34 <= (temp_hpc3_w_4_order15 ^ p34_inp);
        temp_hpc3_v_4_order16 <= (b0_inp ^ r04_inp);
        a_share_reg_hpc3_v_4_order16 <= a4_inp;
        w40 <= (temp_hpc3_w_4_order16 ^ p04_inp);
        temp_hpc3_v_4_order17 <= (b1_inp ^ r14_inp);
        a_share_reg_hpc3_v_4_order17 <= a4_inp;
        w41 <= (temp_hpc3_w_4_order17 ^ p14_inp);
        temp_hpc3_v_4_order18 <= (b2_inp ^ r24_inp);
        a_share_reg_hpc3_v_4_order18 <= a4_inp;
        w42 <= (temp_hpc3_w_4_order18 ^ p24_inp);
        temp_hpc3_v_4_order19 <= (b3_inp ^ r34_inp);
        a_share_reg_hpc3_v_4_order19 <= a4_inp;
        w43 <= (temp_hpc3_w_4_order19 ^ p34_inp);
        u44 <= (a4_inp & b4_inp);
        c0 <= (t3 ^ u04);
        c1 <= (t6 ^ u14);
        c2 <= (t9 ^ u24);
        c3 <= (t12 ^ u34);
        c4 <= (t15 ^ u44);
    end

endmodule


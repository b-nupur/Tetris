module HPC1(
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
    r0,
    r1,
    r2,
    r3,
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
    input  [7:0] r0;
    input  [7:0] r1;
    input  [7:0] r2;
    input  [7:0] r3;
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
    wire [7:0] r0_inp;
    wire [7:0] r1_inp;
    wire [7:0] r2_inp;
    wire [7:0] r3_inp;
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
    wire [7:0] t0;
    wire [7:0] t1;
    wire [7:0] r4;
    reg [7:0] b_share__hpc1_same_shares_4_order0;
    reg [7:0] a0_inp_reg;
    wire [7:0] v00;
    reg [7:0] b_share__hpc1_cross_domain_4_order0;
    wire [7:0] a_and_b_hpc1_cross_domain_4_order0;
    reg [7:0] p01_inp_reg;
    wire [7:0] v01;
    reg [7:0] b_share__hpc1_cross_domain_4_order1;
    wire [7:0] a_and_b_hpc1_cross_domain_4_order1;
    reg [7:0] p02_inp_reg;
    wire [7:0] v02;
    reg [7:0] b_share__hpc1_cross_domain_4_order2;
    wire [7:0] a_and_b_hpc1_cross_domain_4_order2;
    reg [7:0] p03_inp_reg;
    wire [7:0] v03;
    reg [7:0] b_share__hpc1_cross_domain_4_order3;
    wire [7:0] a_and_b_hpc1_cross_domain_4_order3;
    reg [7:0] p04_inp_reg;
    wire [7:0] v04;
    reg [7:0] b_share__hpc1_cross_domain_4_order4;
    reg [7:0] a1_inp_reg;
    wire [7:0] a_and_b_hpc1_cross_domain_4_order4;
    wire [7:0] v10;
    reg [7:0] b_share__hpc1_same_shares_4_order1;
    wire [7:0] v11;
    reg [7:0] b_share__hpc1_cross_domain_4_order5;
    wire [7:0] a_and_b_hpc1_cross_domain_4_order5;
    reg [7:0] p12_inp_reg;
    wire [7:0] v12;
    reg [7:0] b_share__hpc1_cross_domain_4_order6;
    wire [7:0] a_and_b_hpc1_cross_domain_4_order6;
    reg [7:0] p13_inp_reg;
    wire [7:0] v13;
    reg [7:0] b_share__hpc1_cross_domain_4_order7;
    wire [7:0] a_and_b_hpc1_cross_domain_4_order7;
    reg [7:0] p14_inp_reg;
    wire [7:0] v14;
    reg [7:0] b_share__hpc1_cross_domain_4_order8;
    reg [7:0] a2_inp_reg;
    wire [7:0] a_and_b_hpc1_cross_domain_4_order8;
    wire [7:0] v20;
    reg [7:0] b_share__hpc1_cross_domain_4_order9;
    wire [7:0] a_and_b_hpc1_cross_domain_4_order9;
    wire [7:0] v21;
    reg [7:0] b_share__hpc1_same_shares_4_order2;
    wire [7:0] v22;
    reg [7:0] b_share__hpc1_cross_domain_4_order10;
    wire [7:0] a_and_b_hpc1_cross_domain_4_order10;
    reg [7:0] p23_inp_reg;
    wire [7:0] v23;
    reg [7:0] b_share__hpc1_cross_domain_4_order11;
    wire [7:0] a_and_b_hpc1_cross_domain_4_order11;
    reg [7:0] p24_inp_reg;
    wire [7:0] v24;
    reg [7:0] b_share__hpc1_cross_domain_4_order12;
    reg [7:0] a3_inp_reg;
    wire [7:0] a_and_b_hpc1_cross_domain_4_order12;
    wire [7:0] v30;
    reg [7:0] b_share__hpc1_cross_domain_4_order13;
    wire [7:0] a_and_b_hpc1_cross_domain_4_order13;
    wire [7:0] v31;
    reg [7:0] b_share__hpc1_cross_domain_4_order14;
    wire [7:0] a_and_b_hpc1_cross_domain_4_order14;
    wire [7:0] v32;
    reg [7:0] b_share__hpc1_same_shares_4_order3;
    wire [7:0] v33;
    reg [7:0] b_share__hpc1_cross_domain_4_order15;
    wire [7:0] a_and_b_hpc1_cross_domain_4_order15;
    reg [7:0] p34_inp_reg;
    wire [7:0] v34;
    reg [7:0] b_share__hpc1_cross_domain_4_order16;
    reg [7:0] a4_inp_reg;
    wire [7:0] a_and_b_hpc1_cross_domain_4_order16;
    wire [7:0] v40;
    reg [7:0] b_share__hpc1_cross_domain_4_order17;
    wire [7:0] a_and_b_hpc1_cross_domain_4_order17;
    wire [7:0] v41;
    reg [7:0] b_share__hpc1_cross_domain_4_order18;
    wire [7:0] a_and_b_hpc1_cross_domain_4_order18;
    wire [7:0] v42;
    reg [7:0] b_share__hpc1_cross_domain_4_order19;
    wire [7:0] a_and_b_hpc1_cross_domain_4_order19;
    wire [7:0] v43;
    reg [7:0] b_share__hpc1_same_shares_4_order4;
    wire [7:0] v44;
    wire [7:0] t2;
    wire [7:0] t3;
    wire [7:0] t4;
    wire [7:0] z435_assgn435;
    wire [7:0] t5;
    wire [7:0] t6;
    wire [7:0] t7;
    wire [7:0] z443_assgn443;
    wire [7:0] t8;
    wire [7:0] t9;
    wire [7:0] t10;
    wire [7:0] z451_assgn451;
    wire [7:0] t11;
    wire [7:0] t12;
    wire [7:0] t13;
    wire [7:0] z459_assgn459;
    wire [7:0] t14;
    wire [7:0] t15;
    wire [7:0] t16;
    wire [7:0] z467_assgn467;

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
    assign r0_inp = r0;
    assign r1_inp = r1;
    assign r2_inp = r2;
    assign r3_inp = r3;
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
    assign t0 = (r0_inp ^ r1_inp);
    assign t1 = (t0 ^ r2_inp);
    assign r4 = (t1 ^ r3_inp);
    assign v00 = (a0_inp_reg & b_share__hpc1_same_shares_4_order0);
    assign a_and_b_hpc1_cross_domain_4_order0 = (a0_inp_reg & b_share__hpc1_cross_domain_4_order0);
    assign v01 = (a_and_b_hpc1_cross_domain_4_order0 ^ p01_inp_reg);
    assign a_and_b_hpc1_cross_domain_4_order1 = (a0_inp_reg & b_share__hpc1_cross_domain_4_order1);
    assign v02 = (a_and_b_hpc1_cross_domain_4_order1 ^ p02_inp_reg);
    assign a_and_b_hpc1_cross_domain_4_order2 = (a0_inp_reg & b_share__hpc1_cross_domain_4_order2);
    assign v03 = (a_and_b_hpc1_cross_domain_4_order2 ^ p03_inp_reg);
    assign a_and_b_hpc1_cross_domain_4_order3 = (a0_inp_reg & b_share__hpc1_cross_domain_4_order3);
    assign v04 = (a_and_b_hpc1_cross_domain_4_order3 ^ p04_inp_reg);
    assign a_and_b_hpc1_cross_domain_4_order4 = (a1_inp_reg & b_share__hpc1_cross_domain_4_order4);
    assign v10 = (a_and_b_hpc1_cross_domain_4_order4 ^ p01_inp_reg);
    assign v11 = (a1_inp_reg & b_share__hpc1_same_shares_4_order1);
    assign a_and_b_hpc1_cross_domain_4_order5 = (a1_inp_reg & b_share__hpc1_cross_domain_4_order5);
    assign v12 = (a_and_b_hpc1_cross_domain_4_order5 ^ p12_inp_reg);
    assign a_and_b_hpc1_cross_domain_4_order6 = (a1_inp_reg & b_share__hpc1_cross_domain_4_order6);
    assign v13 = (a_and_b_hpc1_cross_domain_4_order6 ^ p13_inp_reg);
    assign a_and_b_hpc1_cross_domain_4_order7 = (a1_inp_reg & b_share__hpc1_cross_domain_4_order7);
    assign v14 = (a_and_b_hpc1_cross_domain_4_order7 ^ p14_inp_reg);
    assign a_and_b_hpc1_cross_domain_4_order8 = (a2_inp_reg & b_share__hpc1_cross_domain_4_order8);
    assign v20 = (a_and_b_hpc1_cross_domain_4_order8 ^ p02_inp_reg);
    assign a_and_b_hpc1_cross_domain_4_order9 = (a2_inp_reg & b_share__hpc1_cross_domain_4_order9);
    assign v21 = (a_and_b_hpc1_cross_domain_4_order9 ^ p12_inp_reg);
    assign v22 = (a2_inp_reg & b_share__hpc1_same_shares_4_order2);
    assign a_and_b_hpc1_cross_domain_4_order10 = (a2_inp_reg & b_share__hpc1_cross_domain_4_order10);
    assign v23 = (a_and_b_hpc1_cross_domain_4_order10 ^ p23_inp_reg);
    assign a_and_b_hpc1_cross_domain_4_order11 = (a2_inp_reg & b_share__hpc1_cross_domain_4_order11);
    assign v24 = (a_and_b_hpc1_cross_domain_4_order11 ^ p24_inp_reg);
    assign a_and_b_hpc1_cross_domain_4_order12 = (a3_inp_reg & b_share__hpc1_cross_domain_4_order12);
    assign v30 = (a_and_b_hpc1_cross_domain_4_order12 ^ p03_inp_reg);
    assign a_and_b_hpc1_cross_domain_4_order13 = (a3_inp_reg & b_share__hpc1_cross_domain_4_order13);
    assign v31 = (a_and_b_hpc1_cross_domain_4_order13 ^ p13_inp_reg);
    assign a_and_b_hpc1_cross_domain_4_order14 = (a3_inp_reg & b_share__hpc1_cross_domain_4_order14);
    assign v32 = (a_and_b_hpc1_cross_domain_4_order14 ^ p23_inp_reg);
    assign v33 = (a3_inp_reg & b_share__hpc1_same_shares_4_order3);
    assign a_and_b_hpc1_cross_domain_4_order15 = (a3_inp_reg & b_share__hpc1_cross_domain_4_order15);
    assign v34 = (a_and_b_hpc1_cross_domain_4_order15 ^ p34_inp_reg);
    assign a_and_b_hpc1_cross_domain_4_order16 = (a4_inp_reg & b_share__hpc1_cross_domain_4_order16);
    assign v40 = (a_and_b_hpc1_cross_domain_4_order16 ^ p04_inp_reg);
    assign a_and_b_hpc1_cross_domain_4_order17 = (a4_inp_reg & b_share__hpc1_cross_domain_4_order17);
    assign v41 = (a_and_b_hpc1_cross_domain_4_order17 ^ p14_inp_reg);
    assign a_and_b_hpc1_cross_domain_4_order18 = (a4_inp_reg & b_share__hpc1_cross_domain_4_order18);
    assign v42 = (a_and_b_hpc1_cross_domain_4_order18 ^ p24_inp_reg);
    assign a_and_b_hpc1_cross_domain_4_order19 = (a4_inp_reg & b_share__hpc1_cross_domain_4_order19);
    assign v43 = (a_and_b_hpc1_cross_domain_4_order19 ^ p34_inp_reg);
    assign v44 = (a4_inp_reg & b_share__hpc1_same_shares_4_order4);
    assign t2 = (v00 ^ v01);
    assign t3 = (t2 ^ v02);
    assign t4 = (t3 ^ v03);
    assign z435_assgn435 = (t4 ^ v04);
    assign t5 = (v10 ^ v11);
    assign t6 = (t5 ^ v12);
    assign t7 = (t6 ^ v13);
    assign z443_assgn443 = (t7 ^ v14);
    assign t8 = (v20 ^ v21);
    assign t9 = (t8 ^ v22);
    assign t10 = (t9 ^ v23);
    assign z451_assgn451 = (t10 ^ v24);
    assign t11 = (v30 ^ v31);
    assign t12 = (t11 ^ v32);
    assign t13 = (t12 ^ v33);
    assign z459_assgn459 = (t13 ^ v34);
    assign t14 = (v40 ^ v41);
    assign t15 = (t14 ^ v42);
    assign t16 = (t15 ^ v43);
    assign z467_assgn467 = (t16 ^ v44);

    always @(posedge clk) begin
        b_share__hpc1_same_shares_4_order0 <= (b0_inp ^ r0_inp);
        a0_inp_reg <= a0_inp;
        b_share__hpc1_cross_domain_4_order0 <= (b1_inp ^ r1_inp);
        p01_inp_reg <= p01_inp;
        b_share__hpc1_cross_domain_4_order1 <= (b2_inp ^ r2_inp);
        p02_inp_reg <= p02_inp;
        b_share__hpc1_cross_domain_4_order2 <= (b3_inp ^ r3_inp);
        p03_inp_reg <= p03_inp;
        b_share__hpc1_cross_domain_4_order3 <= (b4_inp ^ r4);
        p04_inp_reg <= p04_inp;
        b_share__hpc1_cross_domain_4_order4 <= (b0_inp ^ r0_inp);
        a1_inp_reg <= a1_inp;
        b_share__hpc1_same_shares_4_order1 <= (b1_inp ^ r1_inp);
        b_share__hpc1_cross_domain_4_order5 <= (b2_inp ^ r2_inp);
        p12_inp_reg <= p12_inp;
        b_share__hpc1_cross_domain_4_order6 <= (b3_inp ^ r3_inp);
        p13_inp_reg <= p13_inp;
        b_share__hpc1_cross_domain_4_order7 <= (b4_inp ^ r4);
        p14_inp_reg <= p14_inp;
        b_share__hpc1_cross_domain_4_order8 <= (b0_inp ^ r0_inp);
        a2_inp_reg <= a2_inp;
        b_share__hpc1_cross_domain_4_order9 <= (b1_inp ^ r1_inp);
        b_share__hpc1_same_shares_4_order2 <= (b2_inp ^ r2_inp);
        b_share__hpc1_cross_domain_4_order10 <= (b3_inp ^ r3_inp);
        p23_inp_reg <= p23_inp;
        b_share__hpc1_cross_domain_4_order11 <= (b4_inp ^ r4);
        p24_inp_reg <= p24_inp;
        b_share__hpc1_cross_domain_4_order12 <= (b0_inp ^ r0_inp);
        a3_inp_reg <= a3_inp;
        b_share__hpc1_cross_domain_4_order13 <= (b1_inp ^ r1_inp);
        b_share__hpc1_cross_domain_4_order14 <= (b2_inp ^ r2_inp);
        b_share__hpc1_same_shares_4_order3 <= (b3_inp ^ r3_inp);
        b_share__hpc1_cross_domain_4_order15 <= (b4_inp ^ r4);
        p34_inp_reg <= p34_inp;
        b_share__hpc1_cross_domain_4_order16 <= (b0_inp ^ r0_inp);
        a4_inp_reg <= a4_inp;
        b_share__hpc1_cross_domain_4_order17 <= (b1_inp ^ r1_inp);
        b_share__hpc1_cross_domain_4_order18 <= (b2_inp ^ r2_inp);
        b_share__hpc1_cross_domain_4_order19 <= (b3_inp ^ r3_inp);
        b_share__hpc1_same_shares_4_order4 <= (b4_inp ^ r4);
        c0 <= z435_assgn435;
        c1 <= z443_assgn443;
        c2 <= z451_assgn451;
        c3 <= z459_assgn459;
        c4 <= z467_assgn467;
    end

endmodule


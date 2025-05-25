module HPC2(
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
//OUTPUTS
    output reg  [7:0] c0;
    output reg  [7:0] c1;
    output reg  [7:0] c2;
//Intermediate values
    wire [7:0] a0_inp;
    wire [7:0] a1_inp;
    wire [7:0] a2_inp;
    wire [7:0] b0_inp;
    wire [7:0] b1_inp;
    wire [7:0] b2_inp;
    wire [7:0] r01_inp;
    wire [7:0] r02_inp;
    wire [7:0] r12_inp;
    reg [7:0] b_share_reg_hpc2_same_shares_2_order0;
    reg [7:0] a0_inp_reg;
    wire [7:0] z1_assgn1;
    reg [7:0] u00;
    reg [7:0] temp_hpc2_v_2_order0;
    wire [7:0] z3_assgn3;
    reg [7:0] v01;
    reg [7:0] rand_reg_hpc2_w_2_order0;
    wire [7:0] a_neg_hpc2_w_2_order0;
    reg [7:0] a_neg_hpc2_w_2_order0_reg;
    wire [7:0] z5_assgn5;
    reg [7:0] w01;
    wire [7:0] u01;
    reg [7:0] temp_hpc2_v_2_order1;
    wire [7:0] z7_assgn7;
    reg [7:0] v02;
    reg [7:0] rand_reg_hpc2_w_2_order1;
    wire [7:0] a_neg_hpc2_w_2_order1;
    reg [7:0] a_neg_hpc2_w_2_order1_reg;
    wire [7:0] z9_assgn9;
    reg [7:0] w02;
    wire [7:0] u02;
    reg [7:0] temp_hpc2_v_2_order2;
    reg [7:0] a1_inp_reg;
    wire [7:0] z11_assgn11;
    reg [7:0] v10;
    reg [7:0] rand_reg_hpc2_w_2_order2;
    wire [7:0] a_neg_hpc2_w_2_order2;
    reg [7:0] a_neg_hpc2_w_2_order2_reg;
    wire [7:0] z13_assgn13;
    reg [7:0] w10;
    wire [7:0] u10;
    reg [7:0] b_share_reg_hpc2_same_shares_2_order1;
    wire [7:0] z15_assgn15;
    reg [7:0] u11;
    reg [7:0] temp_hpc2_v_2_order3;
    wire [7:0] z17_assgn17;
    reg [7:0] v12;
    reg [7:0] rand_reg_hpc2_w_2_order3;
    wire [7:0] a_neg_hpc2_w_2_order3;
    reg [7:0] a_neg_hpc2_w_2_order3_reg;
    wire [7:0] z19_assgn19;
    reg [7:0] w12;
    wire [7:0] u12;
    reg [7:0] temp_hpc2_v_2_order4;
    reg [7:0] a2_inp_reg;
    wire [7:0] z21_assgn21;
    reg [7:0] v20;
    reg [7:0] rand_reg_hpc2_w_2_order4;
    wire [7:0] a_neg_hpc2_w_2_order4;
    reg [7:0] a_neg_hpc2_w_2_order4_reg;
    wire [7:0] z23_assgn23;
    reg [7:0] w20;
    wire [7:0] u20;
    reg [7:0] temp_hpc2_v_2_order5;
    wire [7:0] z25_assgn25;
    reg [7:0] v21;
    reg [7:0] rand_reg_hpc2_w_2_order5;
    wire [7:0] a_neg_hpc2_w_2_order5;
    reg [7:0] a_neg_hpc2_w_2_order5_reg;
    wire [7:0] z27_assgn27;
    reg [7:0] w21;
    wire [7:0] u21;
    reg [7:0] b_share_reg_hpc2_same_shares_2_order2;
    wire [7:0] z29_assgn29;
    reg [7:0] u22;
    wire [7:0] t1;
    wire [7:0] t2;
    wire [7:0] t3;

    assign a0_inp = a0;
    assign a1_inp = a1;
    assign a2_inp = a2;
    assign b0_inp = b0;
    assign b1_inp = b1;
    assign b2_inp = b2;
    assign r01_inp = r01;
    assign r02_inp = r02;
    assign r12_inp = r12;
    assign z1_assgn1 = (a0_inp_reg & b_share_reg_hpc2_same_shares_2_order0);
    assign z3_assgn3 = (temp_hpc2_v_2_order0 & a0_inp_reg);
    assign a_neg_hpc2_w_2_order0 = !a0_inp;
    assign z5_assgn5 = (a_neg_hpc2_w_2_order0_reg & rand_reg_hpc2_w_2_order0);
    assign u01 = (v01 ^ w01);
    assign z7_assgn7 = (temp_hpc2_v_2_order1 & a0_inp_reg);
    assign a_neg_hpc2_w_2_order1 = !a0_inp;
    assign z9_assgn9 = (a_neg_hpc2_w_2_order1_reg & rand_reg_hpc2_w_2_order1);
    assign u02 = (v02 ^ w02);
    assign z11_assgn11 = (temp_hpc2_v_2_order2 & a1_inp_reg);
    assign a_neg_hpc2_w_2_order2 = !a1_inp;
    assign z13_assgn13 = (a_neg_hpc2_w_2_order2_reg & rand_reg_hpc2_w_2_order2);
    assign u10 = (v10 ^ w10);
    assign z15_assgn15 = (a1_inp_reg & b_share_reg_hpc2_same_shares_2_order1);
    assign z17_assgn17 = (temp_hpc2_v_2_order3 & a1_inp_reg);
    assign a_neg_hpc2_w_2_order3 = !a1_inp;
    assign z19_assgn19 = (a_neg_hpc2_w_2_order3_reg & rand_reg_hpc2_w_2_order3);
    assign u12 = (v12 ^ w12);
    assign z21_assgn21 = (temp_hpc2_v_2_order4 & a2_inp_reg);
    assign a_neg_hpc2_w_2_order4 = !a2_inp;
    assign z23_assgn23 = (a_neg_hpc2_w_2_order4_reg & rand_reg_hpc2_w_2_order4);
    assign u20 = (v20 ^ w20);
    assign z25_assgn25 = (temp_hpc2_v_2_order5 & a2_inp_reg);
    assign a_neg_hpc2_w_2_order5 = !a2_inp;
    assign z27_assgn27 = (a_neg_hpc2_w_2_order5_reg & rand_reg_hpc2_w_2_order5);
    assign u21 = (v21 ^ w21);
    assign z29_assgn29 = (a2_inp_reg & b_share_reg_hpc2_same_shares_2_order2);
    assign t1 = (u00 ^ u01);
    assign t2 = (u10 ^ u11);
    assign t3 = (u20 ^ u21);

    always @(posedge clk) begin
        b_share_reg_hpc2_same_shares_2_order0 <= b0_inp;
        a0_inp_reg <= a0_inp;
        u00 <= z1_assgn1;
        temp_hpc2_v_2_order0 <= (b1_inp ^ r01_inp);
        v01 <= z3_assgn3;
        rand_reg_hpc2_w_2_order0 <= r01_inp;
        a_neg_hpc2_w_2_order0_reg <= a_neg_hpc2_w_2_order0;
        w01 <= z5_assgn5;
        temp_hpc2_v_2_order1 <= (b2_inp ^ r02_inp);
        v02 <= z7_assgn7;
        rand_reg_hpc2_w_2_order1 <= r02_inp;
        a_neg_hpc2_w_2_order1_reg <= a_neg_hpc2_w_2_order1;
        w02 <= z9_assgn9;
        temp_hpc2_v_2_order2 <= (b0_inp ^ r01_inp);
        a1_inp_reg <= a1_inp;
        v10 <= z11_assgn11;
        rand_reg_hpc2_w_2_order2 <= r01_inp;
        a_neg_hpc2_w_2_order2_reg <= a_neg_hpc2_w_2_order2;
        w10 <= z13_assgn13;
        b_share_reg_hpc2_same_shares_2_order1 <= b1_inp;
        u11 <= z15_assgn15;
        temp_hpc2_v_2_order3 <= (b2_inp ^ r12_inp);
        v12 <= z17_assgn17;
        rand_reg_hpc2_w_2_order3 <= r12_inp;
        a_neg_hpc2_w_2_order3_reg <= a_neg_hpc2_w_2_order3;
        w12 <= z19_assgn19;
        temp_hpc2_v_2_order4 <= (b0_inp ^ r02_inp);
        a2_inp_reg <= a2_inp;
        v20 <= z21_assgn21;
        rand_reg_hpc2_w_2_order4 <= r02_inp;
        a_neg_hpc2_w_2_order4_reg <= a_neg_hpc2_w_2_order4;
        w20 <= z23_assgn23;
        temp_hpc2_v_2_order5 <= (b1_inp ^ r12_inp);
        v21 <= z25_assgn25;
        rand_reg_hpc2_w_2_order5 <= r12_inp;
        a_neg_hpc2_w_2_order5_reg <= a_neg_hpc2_w_2_order5;
        w21 <= z27_assgn27;
        b_share_reg_hpc2_same_shares_2_order2 <= b2_inp;
        u22 <= z29_assgn29;
        c0 <= (t1 ^ u02);
        c1 <= (t2 ^ u12);
        c2 <= (t3 ^ u22);
    end

endmodule


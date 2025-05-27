module HPC1(
    clk,
    a0,
    a1,
    a2,
    b0,
    b1,
    b2,
    r0,
    r1,
    p01,
    p02,
    p12,
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
    input  [7:0] r0;
    input  [7:0] r1;
    input  [7:0] p01;
    input  [7:0] p02;
    input  [7:0] p12;
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
    wire [7:0] r0_inp;
    wire [7:0] r1_inp;
    wire [7:0] p01_inp;
    wire [7:0] p02_inp;
    wire [7:0] p12_inp;
    wire [7:0] r2;
    reg [7:0] b_share__hpc1_same_shares_2_order0;
    reg [7:0] a0_inp_reg;
    wire [7:0] v00;
    reg [7:0] b_share__hpc1_cross_domain_2_order0;
    wire [7:0] a_and_b_hpc1_cross_domain_2_order0;
    reg [7:0] p01_inp_reg;
    wire [7:0] v01;
    reg [7:0] b_share__hpc1_cross_domain_2_order1;
    wire [7:0] a_and_b_hpc1_cross_domain_2_order1;
    reg [7:0] p02_inp_reg;
    wire [7:0] v02;
    reg [7:0] b_share__hpc1_cross_domain_2_order2;
    reg [7:0] a1_inp_reg;
    wire [7:0] a_and_b_hpc1_cross_domain_2_order2;
    wire [7:0] v10;
    reg [7:0] b_share__hpc1_same_shares_2_order1;
    wire [7:0] v11;
    reg [7:0] b_share__hpc1_cross_domain_2_order3;
    wire [7:0] a_and_b_hpc1_cross_domain_2_order3;
    reg [7:0] p12_inp_reg;
    wire [7:0] v12;
    reg [7:0] b_share__hpc1_cross_domain_2_order4;
    reg [7:0] a2_inp_reg;
    wire [7:0] a_and_b_hpc1_cross_domain_2_order4;
    wire [7:0] v20;
    reg [7:0] b_share__hpc1_cross_domain_2_order5;
    wire [7:0] a_and_b_hpc1_cross_domain_2_order5;
    wire [7:0] v21;
    reg [7:0] b_share__hpc1_same_shares_2_order2;
    wire [7:0] v22;
    wire [7:0] t1;
    wire [7:0] z159_assgn159;
    wire [7:0] t2;
    wire [7:0] z163_assgn163;
    wire [7:0] t3;
    wire [7:0] z167_assgn167;

    assign a0_inp = a0;
    assign a1_inp = a1;
    assign a2_inp = a2;
    assign b0_inp = b0;
    assign b1_inp = b1;
    assign b2_inp = b2;
    assign r0_inp = r0;
    assign r1_inp = r1;
    assign p01_inp = p01;
    assign p02_inp = p02;
    assign p12_inp = p12;
    assign r2 = (r0_inp ^ r1_inp);
    assign v00 = (a0_inp_reg & b_share__hpc1_same_shares_2_order0);
    assign a_and_b_hpc1_cross_domain_2_order0 = (a0_inp_reg & b_share__hpc1_cross_domain_2_order0);
    assign v01 = (a_and_b_hpc1_cross_domain_2_order0 ^ p01_inp_reg);
    assign a_and_b_hpc1_cross_domain_2_order1 = (a0_inp_reg & b_share__hpc1_cross_domain_2_order1);
    assign v02 = (a_and_b_hpc1_cross_domain_2_order1 ^ p02_inp_reg);
    assign a_and_b_hpc1_cross_domain_2_order2 = (a1_inp_reg & b_share__hpc1_cross_domain_2_order2);
    assign v10 = (a_and_b_hpc1_cross_domain_2_order2 ^ p01_inp_reg);
    assign v11 = (a1_inp_reg & b_share__hpc1_same_shares_2_order1);
    assign a_and_b_hpc1_cross_domain_2_order3 = (a1_inp_reg & b_share__hpc1_cross_domain_2_order3);
    assign v12 = (a_and_b_hpc1_cross_domain_2_order3 ^ p12_inp_reg);
    assign a_and_b_hpc1_cross_domain_2_order4 = (a2_inp_reg & b_share__hpc1_cross_domain_2_order4);
    assign v20 = (a_and_b_hpc1_cross_domain_2_order4 ^ p02_inp_reg);
    assign a_and_b_hpc1_cross_domain_2_order5 = (a2_inp_reg & b_share__hpc1_cross_domain_2_order5);
    assign v21 = (a_and_b_hpc1_cross_domain_2_order5 ^ p12_inp_reg);
    assign v22 = (a2_inp_reg & b_share__hpc1_same_shares_2_order2);
    assign t1 = (v00 ^ v01);
    assign z159_assgn159 = (t1 ^ v02);
    assign t2 = (v10 ^ v11);
    assign z163_assgn163 = (t2 ^ v12);
    assign t3 = (v20 ^ v21);
    assign z167_assgn167 = (t3 ^ v22);

    always @(posedge clk) begin
        b_share__hpc1_same_shares_2_order0 <= (b0_inp ^ r0_inp);
        a0_inp_reg <= a0_inp;
        b_share__hpc1_cross_domain_2_order0 <= (b1_inp ^ r1_inp);
        p01_inp_reg <= p01_inp;
        b_share__hpc1_cross_domain_2_order1 <= (b2_inp ^ r2);
        p02_inp_reg <= p02_inp;
        b_share__hpc1_cross_domain_2_order2 <= (b0_inp ^ r0_inp);
        a1_inp_reg <= a1_inp;
        b_share__hpc1_same_shares_2_order1 <= (b1_inp ^ r1_inp);
        b_share__hpc1_cross_domain_2_order3 <= (b2_inp ^ r2);
        p12_inp_reg <= p12_inp;
        b_share__hpc1_cross_domain_2_order4 <= (b0_inp ^ r0_inp);
        a2_inp_reg <= a2_inp;
        b_share__hpc1_cross_domain_2_order5 <= (b1_inp ^ r1_inp);
        b_share__hpc1_same_shares_2_order2 <= (b2_inp ^ r2);
        c0 <= z159_assgn159;
        c1 <= z163_assgn163;
        c2 <= z167_assgn167;
    end

endmodule


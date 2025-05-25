module HPC3(
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
    input  [7:0] r01;
    input  [7:0] r02;
    input  [7:0] r12;
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
    wire [7:0] r01_inp;
    wire [7:0] r02_inp;
    wire [7:0] r12_inp;
    wire [7:0] p01_inp;
    wire [7:0] p02_inp;
    wire [7:0] p12_inp;
    reg [7:0] u00;
    reg [7:0] temp_hpc3_v_2_order0;
    reg [7:0] a_share_reg_hpc3_v_2_order0;
    wire [7:0] v01;
    wire [7:0] a_share_neg_hpc3_w_2_order0;
    wire [7:0] temp_hpc3_w_2_order0;
    reg [7:0] w01;
    wire [7:0] u01;
    reg [7:0] temp_hpc3_v_2_order1;
    reg [7:0] a_share_reg_hpc3_v_2_order1;
    wire [7:0] v02;
    wire [7:0] a_share_neg_hpc3_w_2_order1;
    wire [7:0] temp_hpc3_w_2_order1;
    reg [7:0] w02;
    wire [7:0] u02;
    reg [7:0] temp_hpc3_v_2_order2;
    reg [7:0] a_share_reg_hpc3_v_2_order2;
    wire [7:0] v10;
    wire [7:0] a_share_neg_hpc3_w_2_order2;
    wire [7:0] temp_hpc3_w_2_order2;
    reg [7:0] w10;
    wire [7:0] u10;
    reg [7:0] u11;
    reg [7:0] temp_hpc3_v_2_order3;
    reg [7:0] a_share_reg_hpc3_v_2_order3;
    wire [7:0] v12;
    wire [7:0] a_share_neg_hpc3_w_2_order3;
    wire [7:0] temp_hpc3_w_2_order3;
    reg [7:0] w12;
    wire [7:0] u12;
    reg [7:0] temp_hpc3_v_2_order4;
    reg [7:0] a_share_reg_hpc3_v_2_order4;
    wire [7:0] v20;
    wire [7:0] a_share_neg_hpc3_w_2_order4;
    wire [7:0] temp_hpc3_w_2_order4;
    reg [7:0] w20;
    wire [7:0] u20;
    reg [7:0] temp_hpc3_v_2_order5;
    reg [7:0] a_share_reg_hpc3_v_2_order5;
    wire [7:0] v21;
    wire [7:0] a_share_neg_hpc3_w_2_order5;
    wire [7:0] temp_hpc3_w_2_order5;
    reg [7:0] w21;
    wire [7:0] u21;
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
    assign p01_inp = p01;
    assign p02_inp = p02;
    assign p12_inp = p12;
    assign v01 = (temp_hpc3_v_2_order0 & a_share_reg_hpc3_v_2_order0);
    assign a_share_neg_hpc3_w_2_order0 = !a0_inp;
    assign temp_hpc3_w_2_order0 = (a_share_neg_hpc3_w_2_order0 & r01_inp);
    assign u01 = (v01 ^ w01);
    assign v02 = (temp_hpc3_v_2_order1 & a_share_reg_hpc3_v_2_order1);
    assign a_share_neg_hpc3_w_2_order1 = !a0_inp;
    assign temp_hpc3_w_2_order1 = (a_share_neg_hpc3_w_2_order1 & r02_inp);
    assign u02 = (v02 ^ w02);
    assign v10 = (temp_hpc3_v_2_order2 & a_share_reg_hpc3_v_2_order2);
    assign a_share_neg_hpc3_w_2_order2 = !a1_inp;
    assign temp_hpc3_w_2_order2 = (a_share_neg_hpc3_w_2_order2 & r01_inp);
    assign u10 = (v10 ^ w10);
    assign v12 = (temp_hpc3_v_2_order3 & a_share_reg_hpc3_v_2_order3);
    assign a_share_neg_hpc3_w_2_order3 = !a1_inp;
    assign temp_hpc3_w_2_order3 = (a_share_neg_hpc3_w_2_order3 & r12_inp);
    assign u12 = (v12 ^ w12);
    assign v20 = (temp_hpc3_v_2_order4 & a_share_reg_hpc3_v_2_order4);
    assign a_share_neg_hpc3_w_2_order4 = !a2_inp;
    assign temp_hpc3_w_2_order4 = (a_share_neg_hpc3_w_2_order4 & r02_inp);
    assign u20 = (v20 ^ w20);
    assign v21 = (temp_hpc3_v_2_order5 & a_share_reg_hpc3_v_2_order5);
    assign a_share_neg_hpc3_w_2_order5 = !a2_inp;
    assign temp_hpc3_w_2_order5 = (a_share_neg_hpc3_w_2_order5 & r12_inp);
    assign u21 = (v21 ^ w21);
    assign t1 = (u00 ^ u01);
    assign t2 = (u10 ^ u11);
    assign t3 = (u20 ^ u21);

    always @(posedge clk) begin
        u00 <= (a0_inp & b0_inp);
        temp_hpc3_v_2_order0 <= (b1_inp ^ r01_inp);
        a_share_reg_hpc3_v_2_order0 <= a0_inp;
        w01 <= (temp_hpc3_w_2_order0 ^ p01_inp);
        temp_hpc3_v_2_order1 <= (b2_inp ^ r02_inp);
        a_share_reg_hpc3_v_2_order1 <= a0_inp;
        w02 <= (temp_hpc3_w_2_order1 ^ p02_inp);
        temp_hpc3_v_2_order2 <= (b0_inp ^ r01_inp);
        a_share_reg_hpc3_v_2_order2 <= a1_inp;
        w10 <= (temp_hpc3_w_2_order2 ^ p01_inp);
        u11 <= (a1_inp & b1_inp);
        temp_hpc3_v_2_order3 <= (b2_inp ^ r12_inp);
        a_share_reg_hpc3_v_2_order3 <= a1_inp;
        w12 <= (temp_hpc3_w_2_order3 ^ p12_inp);
        temp_hpc3_v_2_order4 <= (b0_inp ^ r02_inp);
        a_share_reg_hpc3_v_2_order4 <= a2_inp;
        w20 <= (temp_hpc3_w_2_order4 ^ p02_inp);
        temp_hpc3_v_2_order5 <= (b1_inp ^ r12_inp);
        a_share_reg_hpc3_v_2_order5 <= a2_inp;
        w21 <= (temp_hpc3_w_2_order5 ^ p12_inp);
        u22 <= (a2_inp & b2_inp);
        c0 <= (t1 ^ u02);
        c1 <= (t2 ^ u12);
        c2 <= (t3 ^ u22);
    end

endmodule


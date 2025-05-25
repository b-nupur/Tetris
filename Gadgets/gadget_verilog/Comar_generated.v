module Comar(
    clk,
    a0,
    a1,
    b0,
    b1,
    r0,
    r1,
    r_0,
    r_1,
    r_2,
    r_3,
    c0,
    c1,
);
//INPUTS
    input clk;
    input  [7:0] a0;
    input  [7:0] a1;
    input  [7:0] b0;
    input  [7:0] b1;
    input  [7:0] r0;
    input  [7:0] r1;
    input  [7:0] r_0;
    input  [7:0] r_1;
    input  [7:0] r_2;
    input  [7:0] r_3;
//OUTPUTS
    output reg  [7:0] c0;
    output reg  [7:0] c1;
//Intermediate values
    wire [7:0] a0_inp;
    wire [7:0] a1_inp;
    wire [7:0] b0_inp;
    wire [7:0] b1_inp;
    wire [7:0] r0_inp;
    wire [7:0] r1_inp;
    wire [7:0] r_0_inp;
    wire [7:0] r_1_inp;
    wire [7:0] r_2_inp;
    wire [7:0] r_3_inp;
    reg [7:0] a_0;
    reg [7:0] a_1;
    reg [7:0] b_0;
    reg [7:0] b_1;
    wire [7:0] t0;
    reg [7:0] r_0_inp_reg;
    wire [7:0] z1_assgn1;
    reg [7:0] c_0;
    wire [7:0] t1;
    reg [7:0] r_1_inp_reg;
    wire [7:0] z3_assgn3;
    reg [7:0] c_1;
    wire [7:0] t2;
    reg [7:0] r_2_inp_reg;
    wire [7:0] z5_assgn5;
    reg [7:0] c_2;
    wire [7:0] t3;
    reg [7:0] r_3_inp_reg;
    wire [7:0] z7_assgn7;
    reg [7:0] c_3;
    wire [7:0] t4;
    wire [7:0] t5;
    wire [7:0] t6;
    wire [7:0] t7;
    wire [7:0] z135_assgn135;
    reg [7:0] z135_assgn1350;

    assign a0_inp = a0;
    assign a1_inp = a1;
    assign b0_inp = b0;
    assign b1_inp = b1;
    assign r0_inp = r0;
    assign r1_inp = r1;
    assign r_0_inp = r_0;
    assign r_1_inp = r_1;
    assign r_2_inp = r_2;
    assign r_3_inp = r_3;
    assign t0 = (a_0 & b_0);
    assign z1_assgn1 = (t0 ^ r_0_inp_reg);
    assign t1 = (a_1 & b_0);
    assign z3_assgn3 = (t1 ^ r_1_inp_reg);
    assign t2 = (a_0 & b_1);
    assign z5_assgn5 = (t2 ^ r_2_inp_reg);
    assign t3 = (a_1 & b_1);
    assign z7_assgn7 = (t3 ^ r_3_inp_reg);
    assign t4 = (c_0 ^ c_1);
    assign t5 = (t4 ^ c_2);
    assign t6 = (r_0_inp ^ r_1_inp);
    assign t7 = (t6 ^ r_2_inp);
    assign z135_assgn135 = (t7 ^ r_3_inp);

    always @(posedge clk) begin
        a_0 <= (a0_inp ^ r0_inp);
        a_1 <= (a1_inp ^ r0_inp);
        b_0 <= (b0_inp ^ r1_inp);
        b_1 <= (b1_inp ^ r1_inp);
        r_0_inp_reg <= r_0_inp;
        c_0 <= z1_assgn1;
        r_1_inp_reg <= r_1_inp;
        c_1 <= z3_assgn3;
        r_2_inp_reg <= r_2_inp;
        c_2 <= z5_assgn5;
        r_3_inp_reg <= r_3_inp;
        c_3 <= z7_assgn7;
        c0 <= (t5 ^ c_3);
        z135_assgn1350 <= z135_assgn135;
        c1 <= z135_assgn1350;
    end

endmodule


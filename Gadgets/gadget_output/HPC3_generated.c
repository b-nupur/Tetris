/* HPC3 Function Definition */

void hpc3_same_shares_4_order(int a_share, int b_share, int * u_share) {
    * u_share  = reg(a_share & b_share);
}

void hpc3_v_4_order(int a_share, int b_share, int * v_share, int rand){
    int temp;
    temp = reg(b_share ^ rand);
    int a_share_reg;
	a_share_reg = reg(a_share);
    *v_share = temp & a_share_reg;
}

void hpc3_w_4_order(int a_share, int rand, int prand, int * w_share){
    int temp;
    int a_share_neg;
    a_share_neg = ~(a_share);
    temp = a_share_neg & rand;
    *w_share = reg(temp ^ prand);
}

void hpc3_xor_vw_4_order(int v_share, int w_share, int * u_share){
    *u_share = v_share ^ w_share;
}


void HPC3(int a0, int a1, int a2, int a3, int a4, int b0, int b1, int b2, int b3, int b4, int* c0, int* c1, int* c2, int* c3, int* c4, int r01, int r02, int r03, int r04, int r12, int r13, int r14, int r23, int r24, int r34, int p01, int p02, int p03, int p04, int p12, int p13, int p14, int p23, int p24, int p34){
	int u00, u01, u02, u03, u04, u10, u11, u12, u13, u14, u20, u21, u22, u23, u24, u30, u31, u32, u33, u34, u40, u41, u42, u43, u44;
	int v01, v02, v03, v04, v10, v12, v13, v14, v20, v21, v23, v24, v30, v31, v32, v34, v40, v41, v42, v43;
	int w01, w02, w03, w04, w10, w12, w13, w14, w20, w21, w23, w24, w30, w31, w32, w34, w40, w41, w42, w43;

	hpc3_same_shares_4_order(a0, b0, &u00);

	hpc3_v_4_order(a0, b1, &v01 , r01);
	hpc3_w_4_order(a0, r01, p01, &w01);
	hpc3_xor_vw_4_order(v01, w01, &u01);

	hpc3_v_4_order(a0, b2, &v02 , r02);
	hpc3_w_4_order(a0, r02, p02, &w02);
	hpc3_xor_vw_4_order(v02, w02, &u02);

	hpc3_v_4_order(a0, b3, &v03 , r03);
	hpc3_w_4_order(a0, r03, p03, &w03);
	hpc3_xor_vw_4_order(v03, w03, &u03);

	hpc3_v_4_order(a0, b4, &v04 , r04);
	hpc3_w_4_order(a0, r04, p04, &w04);
	hpc3_xor_vw_4_order(v04, w04, &u04);

	hpc3_v_4_order(a1, b0, &v10 , r01);
	hpc3_w_4_order(a1, r01, p01, &w10);
	hpc3_xor_vw_4_order(v10, w10, &u10);

	hpc3_same_shares_4_order(a1, b1, &u11);

	hpc3_v_4_order(a1, b2, &v12 , r12);
	hpc3_w_4_order(a1, r12, p12, &w12);
	hpc3_xor_vw_4_order(v12, w12, &u12);

	hpc3_v_4_order(a1, b3, &v13 , r13);
	hpc3_w_4_order(a1, r13, p13, &w13);
	hpc3_xor_vw_4_order(v13, w13, &u13);

	hpc3_v_4_order(a1, b4, &v14 , r14);
	hpc3_w_4_order(a1, r14, p14, &w14);
	hpc3_xor_vw_4_order(v14, w14, &u14);

	hpc3_v_4_order(a2, b0, &v20 , r02);
	hpc3_w_4_order(a2, r02, p02, &w20);
	hpc3_xor_vw_4_order(v20, w20, &u20);

	hpc3_v_4_order(a2, b1, &v21 , r12);
	hpc3_w_4_order(a2, r12, p12, &w21);
	hpc3_xor_vw_4_order(v21, w21, &u21);

	hpc3_same_shares_4_order(a2, b2, &u22);

	hpc3_v_4_order(a2, b3, &v23 , r23);
	hpc3_w_4_order(a2, r23, p23, &w23);
	hpc3_xor_vw_4_order(v23, w23, &u23);

	hpc3_v_4_order(a2, b4, &v24 , r24);
	hpc3_w_4_order(a2, r24, p24, &w24);
	hpc3_xor_vw_4_order(v24, w24, &u24);

	hpc3_v_4_order(a3, b0, &v30 , r03);
	hpc3_w_4_order(a3, r03, p03, &w30);
	hpc3_xor_vw_4_order(v30, w30, &u30);

	hpc3_v_4_order(a3, b1, &v31 , r13);
	hpc3_w_4_order(a3, r13, p13, &w31);
	hpc3_xor_vw_4_order(v31, w31, &u31);

	hpc3_v_4_order(a3, b2, &v32 , r23);
	hpc3_w_4_order(a3, r23, p23, &w32);
	hpc3_xor_vw_4_order(v32, w32, &u32);

	hpc3_same_shares_4_order(a3, b3, &u33);

	hpc3_v_4_order(a3, b4, &v34 , r34);
	hpc3_w_4_order(a3, r34, p34, &w34);
	hpc3_xor_vw_4_order(v34, w34, &u34);

	hpc3_v_4_order(a4, b0, &v40 , r04);
	hpc3_w_4_order(a4, r04, p04, &w40);
	hpc3_xor_vw_4_order(v40, w40, &u40);

	hpc3_v_4_order(a4, b1, &v41 , r14);
	hpc3_w_4_order(a4, r14, p14, &w41);
	hpc3_xor_vw_4_order(v41, w41, &u41);

	hpc3_v_4_order(a4, b2, &v42 , r24);
	hpc3_w_4_order(a4, r24, p24, &w42);
	hpc3_xor_vw_4_order(v42, w42, &u42);

	hpc3_v_4_order(a4, b3, &v43 , r34);
	hpc3_w_4_order(a4, r34, p34, &w43);
	hpc3_xor_vw_4_order(v43, w43, &u43);

	hpc3_same_shares_4_order(a4, b4, &u44);

	int t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15;
	t1 = u00 ^ u01;
	t2 = t1 ^ u02;
	t3 = t2 ^ u03;
	*c0 = t3 ^ u04;

	t4 = u10 ^ u11;
	t5 = t4 ^ u12;
	t6 = t5 ^ u13;
	*c1 = t6 ^ u14;

	t7 = u20 ^ u21;
	t8 = t7 ^ u22;
	t9 = t8 ^ u23;
	*c2 = t9 ^ u24;

	t10 = u30 ^ u31;
	t11 = t10 ^ u32;
	t12 = t11 ^ u33;
	*c3 = t12 ^ u34;

	t13 = u40 ^ u41;
	t14 = t13 ^ u42;
	t15 = t14 ^ u43;
	*c4 = t15 ^ u44;

}
/* HPC3 Function Definition */

void hpc3_same_shares_2_order(int a_share, int b_share, int * u_share) {
    * u_share  = reg(a_share & b_share);
}

void hpc3_v_2_order(int a_share, int b_share, int * v_share, int rand){
    int temp;
    temp = reg(b_share ^ rand);
    int a_share_reg;
	a_share_reg = reg(a_share);
    *v_share = temp & a_share_reg;
}

void hpc3_w_2_order(int a_share, int rand, int prand, int * w_share){
    int temp;
    int a_share_neg;
    a_share_neg = ~(a_share);
    temp = a_share_neg & rand;
    *w_share = reg(temp ^ prand);
}

void hpc3_xor_vw_2_order(int v_share, int w_share, int * u_share){
    *u_share = v_share ^ w_share;
}


void HPC3(int a0, int a1, int a2, int b0, int b1, int b2, int* c0, int* c1, int* c2, int r01, int r02, int r12, int p01, int p02, int p12){
	int u00, u01, u02, u10, u11, u12, u20, u21, u22;
	int v01, v02, v10, v12, v20, v21;
	int w01, w02, w10, w12, w20, w21;

	hpc3_same_shares_2_order(a0, b0, &u00);

	hpc3_v_2_order(a0, b1, &v01 , r01);
	hpc3_w_2_order(a0, r01, p01, &w01);
	hpc3_xor_vw_2_order(v01, w01, &u01);

	hpc3_v_2_order(a0, b2, &v02 , r02);
	hpc3_w_2_order(a0, r02, p02, &w02);
	hpc3_xor_vw_2_order(v02, w02, &u02);

	hpc3_v_2_order(a1, b0, &v10 , r01);
	hpc3_w_2_order(a1, r01, p01, &w10);
	hpc3_xor_vw_2_order(v10, w10, &u10);

	hpc3_same_shares_2_order(a1, b1, &u11);

	hpc3_v_2_order(a1, b2, &v12 , r12);
	hpc3_w_2_order(a1, r12, p12, &w12);
	hpc3_xor_vw_2_order(v12, w12, &u12);

	hpc3_v_2_order(a2, b0, &v20 , r02);
	hpc3_w_2_order(a2, r02, p02, &w20);
	hpc3_xor_vw_2_order(v20, w20, &u20);

	hpc3_v_2_order(a2, b1, &v21 , r12);
	hpc3_w_2_order(a2, r12, p12, &w21);
	hpc3_xor_vw_2_order(v21, w21, &u21);

	hpc3_same_shares_2_order(a2, b2, &u22);

	int t1, t2, t3;
	t1 = u00 ^ u01;
	*c0 = t1 ^ u02;

	t2 = u10 ^ u11;
	*c1 = t2 ^ u12;

	t3 = u20 ^ u21;
	*c2 = t3 ^ u22;

}
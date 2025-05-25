/* HPC2 Function Definition */

void hpc2_same_shares_2_order(int a_share, int b_share, int * u_share) {
    int b_share_reg;
	b_share_reg = reg(b_share);
	* u_share  = reg(a_share & b_share_reg);
}

void hpc2_v_2_order(int a_share, int b_share, int * v_share, int rand){
    int temp; 
    temp = reg(b_share ^ rand);
    *v_share = reg(temp & a_share);
}

void hpc2_w_2_order(int a_share, int rand, int *  w_share){
    int rand_reg;
	rand_reg = reg(rand);
	int a_neg;
    a_neg = ~(a_share);
    *w_share = reg(a_neg & rand_reg);
}

void hpc2_xor_vw_2_order(int v_share, int w_share, int * u_share){
    *u_share = v_share ^ w_share;
}

void HPC2(int a0, int a1, int a2, int b0, int b1, int b2, int * c0, int * c1, int * c2, int r01, int r02, int r12){
	int u00, u01, u02, u10, u11, u12, u20, u21, u22;
	int v01, v02, v10, v12, v20, v21;

	int w01, w02, w10, w12, w20, w21;

	hpc2_same_shares_2_order(a0, b0, &u00);
	hpc2_v_2_order(a0, b1, &v01 , r01);
	hpc2_w_2_order(a0, r01, &w01);
	hpc2_xor_vw_2_order(v01, w01, &u01);

	hpc2_v_2_order(a0, b2, &v02 , r02);
	hpc2_w_2_order(a0, r02, &w02);
	hpc2_xor_vw_2_order(v02, w02, &u02);

	hpc2_v_2_order(a1, b0, &v10 , r01);
	hpc2_w_2_order(a1, r01, &w10);
	hpc2_xor_vw_2_order(v10, w10, &u10);

	hpc2_same_shares_2_order(a1, b1, &u11);
	hpc2_v_2_order(a1, b2, &v12 , r12);
	hpc2_w_2_order(a1, r12, &w12);
	hpc2_xor_vw_2_order(v12, w12, &u12);

	hpc2_v_2_order(a2, b0, &v20 , r02);
	hpc2_w_2_order(a2, r02, &w20);
	hpc2_xor_vw_2_order(v20, w20, &u20);

	hpc2_v_2_order(a2, b1, &v21 , r12);
	hpc2_w_2_order(a2, r12, &w21);
	hpc2_xor_vw_2_order(v21, w21, &u21);

	hpc2_same_shares_2_order(a2, b2, &u22);
	int t1, t2, t3;

	t1 = u00 ^ u01;
	*c0 = t1 ^ u02;

	t2 = u10 ^ u11;
	*c1 = t2 ^ u12;

	t3 = u20 ^ u21;
	*c2 = t3 ^ u22;

}
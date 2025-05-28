/* HPC1 Function Definition */


// 4 order secure hpc1 code 
// same domain term e.g. (bi = bi & ai)
void hpc1_same_shares_4_order(int a_share, int b_share, int rand, int * v_share) {
    int b_share_;
    b_share_ = reg(b_share ^ rand);
    *v_share  = a_share & b_share_;
}

// cross domain terms ( e.g., vij = ai & bj )
void hpc1_cross_domain_4_order(int a_share, int b_share, int * v_share, int rand, int prand){

    //refresh sharing of b_share
    int b_share_;
    b_share_ = reg(b_share ^ rand);

    int a_and_b;
    a_and_b = a_share & b_share_;
    *v_share = a_and_b ^ prand;
}

        
void HPC1(int a0, int a1, int a2, int a3, int a4, int b0, int b1, int b2, int b3, int b4, int* c0, int* c1, int* c2, int* c3, int* c4, int r0, int r1, int r2, int r3, int p01, int p02, int p03, int p04, int p12, int p13, int p14, int p23, int p24, int p34){
		int v00, v01, v02, v03, v04, v10, v11, v12, v13, v14, v20, v21, v22, v23, v24, v30, v31, v32, v33, v34, v40, v41, v42, v43, v44;
		int r4;
		int t0, t1;
		t0 = r0 ^ r1;
		t1 = t0 ^ r2;
		r4 = t1 ^ r3;
		hpc1_same_shares_4_order(a0, b0, r0, &v00);
		hpc1_cross_domain_4_order(a0, b1, &v01 , r1, p01);
		hpc1_cross_domain_4_order(a0, b2, &v02 , r2, p02);
		hpc1_cross_domain_4_order(a0, b3, &v03 , r3, p03);
		hpc1_cross_domain_4_order(a0, b4, &v04 , r4, p04);
		hpc1_cross_domain_4_order(a1, b0, &v10 , r0, p01);
		hpc1_same_shares_4_order(a1, b1, r1, &v11);
		hpc1_cross_domain_4_order(a1, b2, &v12 , r2, p12);
		hpc1_cross_domain_4_order(a1, b3, &v13 , r3, p13);
		hpc1_cross_domain_4_order(a1, b4, &v14 , r4, p14);
		hpc1_cross_domain_4_order(a2, b0, &v20 , r0, p02);
		hpc1_cross_domain_4_order(a2, b1, &v21 , r1, p12);
		hpc1_same_shares_4_order(a2, b2, r2, &v22);
		hpc1_cross_domain_4_order(a2, b3, &v23 , r3, p23);
		hpc1_cross_domain_4_order(a2, b4, &v24 , r4, p24);
		hpc1_cross_domain_4_order(a3, b0, &v30 , r0, p03);
		hpc1_cross_domain_4_order(a3, b1, &v31 , r1, p13);
		hpc1_cross_domain_4_order(a3, b2, &v32 , r2, p23);
		hpc1_same_shares_4_order(a3, b3, r3, &v33);
		hpc1_cross_domain_4_order(a3, b4, &v34 , r4, p34);
		hpc1_cross_domain_4_order(a4, b0, &v40 , r0, p04);
		hpc1_cross_domain_4_order(a4, b1, &v41 , r1, p14);
		hpc1_cross_domain_4_order(a4, b2, &v42 , r2, p24);
		hpc1_cross_domain_4_order(a4, b3, &v43 , r3, p34);
		hpc1_same_shares_4_order(a4, b4, r4, &v44);

		int t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15, t16;

		t2 = v00 ^ v01;
		t3 = t2 ^ v02;
		t4 = t3 ^ v03;
		*c0 = reg(t4 ^ v04);

		t5 = v10 ^ v11;
		t6 = t5 ^ v12;
		t7 = t6 ^ v13;
		*c1 = reg(t7 ^ v14);

		t8 = v20 ^ v21;
		t9 = t8 ^ v22;
		t10 = t9 ^ v23;
		*c2 = reg(t10 ^ v24);

		t11 = v30 ^ v31;
		t12 = t11 ^ v32;
		t13 = t12 ^ v33;
		*c3 = reg(t13 ^ v34);

		t14 = v40 ^ v41;
		t15 = t14 ^ v42;
		t16 = t15 ^ v43;
		*c4 = reg(t16 ^ v44);

}
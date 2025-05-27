/* HPC1 Function Definition */


// 2 order secure hpc1 code 
// same domain term e.g. (bi = bi & ai)
void hpc1_same_shares_2_order(int a_share, int b_share, int rand, int * v_share) {
    int b_share_;
    b_share_ = reg(b_share ^ rand);
    *v_share  = a_share & b_share_;
}

// cross domain terms ( e.g., vij = ai & bj )
void hpc1_cross_domain_2_order(int a_share, int b_share, int * v_share, int rand, int prand){

    //refresh sharing of b_share
    int b_share_;
    b_share_ = reg(b_share ^ rand);

    int a_and_b;
    a_and_b = a_share & b_share_;
    *v_share = a_and_b ^ prand;
}

        
void HPC1(int a0, int a1, int a2, int b0, int b1, int b2, int* c0, int* c1, int* c2, int r0, int r1, int p01, int p02, int p12){
		int v00, v01, v02, v10, v11, v12, v20, v21, v22;
		int r2;
		r2 = r0 ^ r1;
		hpc1_same_shares_2_order(a0, b0, r0, &v00);
		hpc1_cross_domain_2_order(a0, b1, &v01 , r1, p01);
		hpc1_cross_domain_2_order(a0, b2, &v02 , r2, p02);
		hpc1_cross_domain_2_order(a1, b0, &v10 , r0, p01);
		hpc1_same_shares_2_order(a1, b1, r1, &v11);
		hpc1_cross_domain_2_order(a1, b2, &v12 , r2, p12);
		hpc1_cross_domain_2_order(a2, b0, &v20 , r0, p02);
		hpc1_cross_domain_2_order(a2, b1, &v21 , r1, p12);
		hpc1_same_shares_2_order(a2, b2, r2, &v22);

		int t1, t2, t3;

		t1 = v00 ^ v01;
		*c0 = reg(t1 ^ v02);

		t2 = v10 ^ v11;
		*c1 = reg(t2 ^ v12);

		t3 = v20 ^ v21;
		*c2 = reg(t3 ^ v22);

}
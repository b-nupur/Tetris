/* HPC1 Function Definition */
# include <stdio.h>
# include <stdlib.h>
# include <time.h>

/* HPC1 Function Definition */


// 4 order secure hpc1 code 
// same domain term e.g. (bi = bi & ai)
void hpc1_same_shares_4_order(int a_share, int b_share, int rand, int * v_share) {
    int b_share_;
    b_share_ = (b_share ^ rand);
    *v_share  = a_share & b_share_;
}

// cross domain terms ( e.g., vij = ai & bj )
void hpc1_cross_domain_4_order(int a_share, int b_share, int * v_share, int rand, int prand){

    //refresh sharing of b_share
    int b_share_;
    b_share_ = (b_share ^ rand);

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
		*c0 = (t4 ^ v04);

		t5 = v10 ^ v11;
		t6 = t5 ^ v12;
		t7 = t6 ^ v13;
		*c1 = (t7 ^ v14);

		t8 = v20 ^ v21;
		t9 = t8 ^ v22;
		t10 = t9 ^ v23;
		*c2 = (t10 ^ v24);

		t11 = v30 ^ v31;
		t12 = t11 ^ v32;
		t13 = t12 ^ v33;
		*c3 = (t13 ^ v34);

		t14 = v40 ^ v41;
		t15 = t14 ^ v42;
		t16 = t15 ^ v43;
		*c4 = (t16 ^ v44);

}
int main(){
    srand(time(NULL)); // Seed random number generator

    int a = 12; // Example input
    int b = 13; // Example input
    // int r = rand();

    int a0, a1, a2, a3, a4;
    int b0, b1, b2, b3, b4;
    int c0, c1, c2, c3, c4;

    //shares for A
    a0 = rand();
    a1 = rand();
    a2 = rand();
    a3 = rand();
    a4 = a ^ a0 ^ a1 ^ a2 ^ a3; // Ensure a4 is the XOR of the others

    // shares for B
    b0 = rand();
    b1 = rand();
    b2 = rand();
    b3 = rand();
    b4 = b ^ b0 ^ b1 ^ b2 ^ b3; // Ensure b4 is the XOR of the others

    printf("[INFO]: Original a = %d, Reconstructed a = %d\n", a, a0 ^ a1 ^ a2 ^a3 ^ a4);
    printf("[INFO]: Original b = %d, Reconstructed b = %d\n", b, b0 ^ b1 ^ b2 ^ b3 ^ b4);
    printf("[INFO]: Expected a & b = %d\n", a & b);

    int r0, r1, r2, r3, r4;

    r0 = rand();
    r1 = rand();
    r3 = rand();
    // r2 = r0 ^r1; // R share

    int p01, p02, p03, p04, p12, p13, p14, p23, p24, p34; // Random masks
    p01 = rand();
    p02 = rand();
    p12 = rand();
    p03 = rand();
    p04 = rand();   
    p13 = rand();
    p14 = rand();
    p23 = rand();
    p24 = rand();
    p34 = rand();

    HPC1(a0, a1, a2, a3, a4, b0, b1, b2, b3, b4, &c0, &c1, &c2, &c3, &c4, r0, r1, r2, r3, p01, p02, p03, p04, p12, p13, p14, p23, p24, p34);
    
    int c_reconstructed = c0 ^ c1 ^ c2 ^ c3 ^ c4; // Reconstructing the outpu
    printf("Reconstructed c (a & b) = %d\n", c_reconstructed);

    if ((a & b) == c_reconstructed) {
        printf("[SUCCESS]: HPC1 multiplication is correct.\n");
    } else {
        printf("[FAILURE]: HPC1 multiplication is incorrect.\n");
    }
    
    // Test with more values
    printf("\n--- Batch Test ---\n");
    for (int test_a = 0; test_a <=3; ++test_a) {
        for (int test_b = 0; test_b <=3; ++test_b) {
        
            a0 = rand(); a1 = rand(); a2 = rand(), a3 = rand(); a4 = test_a ^ a0 ^ a1 ^ a2 ^ a3;
            b0 = rand(); b1 = rand(); b2 = rand(); b3 = rand(); b4 = test_b ^ b0 ^ b1 ^ b2 ^ b3;
            r0 = rand(); r1 = rand(); r2 = rand(); r3 = rand(); 

            p01 = rand();
            p02 = rand();
            p12 = rand();
            p03 = rand();
            p04 = rand();   
            p13 = rand();
            p14 = rand();
            p23 = rand();
            p24 = rand();
            p34 = rand();

            HPC1(a0, a1, a2, a3, a4, b0, b1, b2, b3, b4, &c0, &c1, &c2, &c3, &c4, r0, r1, r2, r3, p01, p02, p03, p04, p12, p13, p14, p23, p24, p34);
            c_reconstructed = c0 ^ c1 ^ c2 ^ c3 ^ c4; // Reconstructing the output
            printf("a=%d, b=%d, a&b=%d, c_reconstructed=%d -- %s\n",
                   test_a, test_b, test_a & test_b, c_reconstructed,
                   ((test_a & test_b) == c_reconstructed) ? "PASS" : "FAIL");
        }
    }

    return 0;
}
/* HPC1 Function Definition */
# include <stdio.h>
# include <stdlib.h>
# include <time.h>

    // 2 order secure hpc1 code 
    // same domain term e.g. (bi = bi & ai)
    void hpc1_same_shares_2_order(int a_share, int b_share, int rand, int * v_share) {
        int b_share_;
        b_share_ = (b_share ^ rand);
        *v_share  = a_share & b_share_;
    }
    
    // cross domain terms ( e.g., vij = ai & bj )
    void hpc1_cross_domain_2_order(int a_share, int b_share, int * v_share, int rand, int prand){
    
        //refresh sharing of b_share
        int b_share_;
        b_share_ = (b_share ^ rand);
    
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
            *c0 = (t1 ^ v02);
    
            t2 = v10 ^ v11;
            *c1 = (t2 ^ v12);
    
            t3 = v20 ^ v21;
            *c2 = (t3 ^ v22);
    
    }

int main(){
    srand(time(NULL)); // Seed random number generator

    int a = 12; // Example input
    int b = 13; // Example input
    // int r = rand();

    int a0, a1, a2;
    int b0, b1, b2;
    int c0, c1, c2;

    //shares for A
    a0 = rand();
    a1 = rand();
    a2 = a ^ a0 ^ a1;

    // shares for B
    b0 = rand();
    b1 = rand();
    b2 = b ^ b0 ^ b1;

    printf("[INFO]: Original a = %d, Reconstructed a = %d\n", a, a0 ^ a1 ^ a2);
    printf("[INFO]: Original b = %d, Reconstructed b = %d\n", b, b0 ^ b1 ^ b2);
    printf("[INFO]: Expected a & b = %d\n", a & b);

    int r0, r1, r2;

    r0 = rand();
    r1 = rand();
    r2 = r0 ^r1; // R share

    int p01, p02, p12; // Random masks
    p01 = rand();
    p02 = rand();
    p12 = rand();

    HPC1(a0, a1, a2, b0, b1, b2, &c0, &c1, &c2, r0, r1, p01, p02, p12);
    
    int c_reconstructed = c0 ^ c1 ^ c2;
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
        
            a0 = rand(); a1 = rand(); a2 = test_a ^ a0 ^ a1;
            b0 = rand(); b1 = rand(); b2 = test_b ^ b0 ^ b1;
            r0 = rand(); r1 = rand(); r2 = r0 ^ r1;
            p01 = rand(); p02 = rand(); p12 = rand();
            HPC1(a0, a1, a2, b0, b1, b2, &c0, &c1, &c2, r0, r1, p01, p02, p12);
            c_reconstructed = c0 ^ c1 ^ c2;
            printf("a=%d, b=%d, a&b=%d, c_reconstructed=%d -- %s\n",
                   test_a, test_b, test_a & test_b, c_reconstructed,
                   ((test_a & test_b) == c_reconstructed) ? "PASS" : "FAIL");
        }
    }

    return 0;
}
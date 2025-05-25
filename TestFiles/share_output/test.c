
#include <stdio.h>
#include <stdlib.h> 
#include <time.h>

void hpc2_v_1_order(int a_share, int b_share, int *v_share, int rand);
void hpc2_same_shares_1_order(int a_share, int b_share, int *u_share);
void Comar(int a0, int a1, int b0, int b1, int *c0, int *c1, int r0, int r1, int r_0, int r_1, int r_2, int r_3);
void hpc2_w_1_order(int a_share, int rand, int *w_share);
void hpc2_xor_vw_1_order(int v_share, int w_share, int *u_share);
void HPC2(int a0, int a1, int b0, int b1, int *c0, int *c1, int r01);


void Sbox(int n_0, int n_1, int *__return_value_0, int *__return_value_1, int dec_0, int dec_1, int dec_255, int dec_169, int dec_129, int dec_9, int dec_72, int dec_242, int dec_243, int dec_152, int dec_240, int dec_4, int dec_15, int dec_12, int dec_2, int dec_3, int dec_36, int dec_220, int dec_11, int dec_158, int dec_45, int dec_88, int dec_99, int comar_r1, int comar_r5, int rand_4, int rand_3, int rand_9, int comar_r2, int rand_1, int rand_5, int comar_r6, int comar_r3, int rand_6, int rand_2, int rand_7, int comar_r4, int rand_8);
int official_sbox[256] = {
    99,124,119,123,242,107,111,197, 48,  1,103, 43,254,215,171,118,
   202,130,201,125,250, 89, 71,240,173,212,162,175,156,164,114,192,
   183,253,147, 38, 54, 63,247,204, 52,165,229,241,113,216, 49, 21,
     4,199, 35,195, 24,150,  5,154,  7, 18,128,226,235, 39,178,117,
     9,131, 44, 26, 27,110, 90,160, 82, 59,214,179, 41,227, 47,132,
    83,209,  0,237, 32,252,177, 91,106,203,190, 57, 74, 76, 88,207,
   208,239,170,251, 67, 77, 51,133, 69,249,  2,127, 80, 60,159,168,
    81,163, 64,143,146,157, 56,245,188,182,218, 33, 16,255,243,210,
   205, 12, 19,236, 95,151, 68, 23,196,167,126, 61,100, 93, 25,115,
    96,129, 79,220, 34, 42,144,136, 70,238,184, 20,222, 94, 11,219,
   224, 50, 58, 10, 73,  6, 36, 92,194,211,172, 98,145,149,228,121,
   231,200, 55,109,141,213, 78,169,108, 86,244,234,101,122,174,  8,
   186,120, 37, 46, 28,166,180,198,232,221,116, 31, 75,189,139,138,
   112, 62,181,102, 72,  3,246, 14, 97, 53, 87,185,134,193, 29,158,
   225,248,152, 17,105,217,142,148,155, 30,135,233,206, 85, 40,223,
   140,161,137, 13,191,230, 66,104, 65,153, 45, 15,176, 84,187, 22
  };
  
int main() {
    int result0, result1;
  
    // Initialize all required dec_* constants with sample values
    int dec_0 = 0;
    int dec_1 = 1;
    int dec_255 = 255;
    int dec_169 = 169;
    int dec_129 = 129;
    int dec_9 = 9;
    int dec_72 = 72;
    int dec_242 = 242;
    int dec_243 = 243;
    int dec_152 = 152;
    int dec_240 = 240;
    int dec_4 = 4;
    int dec_15 = 15;
    int dec_12 = 12;
    int dec_2 = 2;
    int dec_3 = 3;
    int dec_36 = 36;
    int dec_220 = 220;
    int dec_11 = 11;
    int dec_158 = 158;
    int dec_45 = 45;
    int dec_88 = 88;
    int dec_99 = 99;
  
    // Input to Sbox function

  
  
    // Call the Sbox function
    for(int i = 0; i < 256; i++){

        int n = i;
        
        int n1 = rand() % 256;
        int n0 = n ^ n1;
        // printf("n = %d ", n1 ^ n0 );
      

        int rand_1 = rand() % 256;
        int rand_2 = rand() % 256;
        int rand_3 = rand() % 256;
        int rand_4 = rand() % 256;
        int rand_5 = rand() % 256;
        int rand_6 = rand() % 256;
        int rand_7 = rand() % 256;
        int rand_8 = rand() % 256;
        int rand_9 = rand() % 256;


        int comar_r1 = rand() % 256;
        int comar_r2 = rand() % 256;
        int comar_r3 = rand() % 256;
        int comar_r4 = rand() % 256;
        int comar_r5 = rand() % 256;
        int comar_r6 = rand() % 256;
        

        Sbox(n0,n1, &result0, &result1,
            dec_0, dec_1, dec_255, dec_169, dec_129, dec_9,
            dec_72, dec_242, dec_243, dec_152, dec_240,
            dec_4, dec_15, dec_12, dec_2, dec_3,
            dec_36, dec_220, dec_11, dec_158, dec_45,
            dec_88, dec_99, comar_r1, comar_r5, rand_4, rand_3, rand_9, comar_r2,rand_1,rand_5, comar_r6,comar_r3, rand_6, rand_2, rand_7, comar_r4, rand_8);
          
            // Print the result
      if ((official_sbox[n0 ^ n1]  != (result0 ^ result1)))
        printf("n = %d n1 = %d Sbox result: %d != %d \n",(n0 ^ n1) ,n1, official_sbox[n0 ^ n1] , (result0 ^ result1));
        
    }

  
  return 0;
  }
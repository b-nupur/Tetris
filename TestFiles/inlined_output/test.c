#include <stdio.h>
#include <stdlib.h> // For rand() and srand()
#include <time.h>

//  command to run : gcc output.c test.c -o test_sbox
// ./test_sbox  
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

void Sbox(int n, int *__return_value, int dec_0, int dec_1, int dec_255, int dec_169, int dec_129, int dec_9, int dec_72, int dec_242, int dec_243, int dec_152, int dec_240, int dec_4, int dec_15, int dec_12, int dec_2, int dec_3, int dec_36, int dec_220, int dec_11, int dec_158, int dec_45, int dec_88, int dec_99);    // Call the Sbox function

int main() {
    int result;
  
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

  
    
    // for(int i = 0; i < 256; i++){

        int n = 10;
    
        Sbox(n, &result,
            dec_0, dec_1, dec_255, dec_169, dec_129, dec_9,
            dec_72, dec_242, dec_243, dec_152, dec_240,
            dec_4, dec_15, dec_12, dec_2, dec_3,
            dec_36, dec_220, dec_11, dec_158, dec_45,
            dec_88, dec_99);
        if (official_sbox[n]  != result)
            printf("Sbox result: %d != %d \n", official_sbox[n] , result);
            
    // }
    printf("Finished testing\n");
  
  return 0;
  }
  
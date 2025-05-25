#include <stdbool.h>
void and_2(bool a, bool b, bool *d)
{
  *d = a & b;
}

void and_3(bool a, bool b, bool c, bool * d)
{
  bool temp;
  and_2(a, b, &temp);
  and_2(temp, c, d);
}

void sbox(bool x0, bool x1, bool x2, bool x3, bool *y0, bool *y1, bool *y2, bool *y3)
{
  bool temp1_y0, temp1_y1, temp2_y1, temp3_y1, temp4_y1, temp5_y1, temp1_y2, temp2_y2, temp3_y2, temp4_y2, temp5_y2, temp1_y3, temp2_y3, temp3_y3, temp4_y3;
  int t1, t2, t8, t9, t10, t11, t12, t18, t19, t20, t21, t22, t23, t28, t29, t30, t31, t32, t33;
  and_2(x1, x2, &temp1_y0);
  
  t2 = x2 ^ x3;
  t1 = t2 ^ temp1_y0;
  *y0 = t1 ^ x0;
  
  and_3(x0, x1, x2, &temp1_y1);
  and_3(x0, x1, x3, &temp2_y1);
  and_3(x0, x2, x3, &temp3_y1);
  and_2(x1, x3, &temp4_y1);
  and_2(x2, x3, &temp5_y1);

  t12 = x1 ^ x3;
  t11 = t12 ^ temp1_y1;
  t10 = t11 ^ temp2_y1;
  t9 = t10 ^ temp3_y1;
  t8 = t9 ^ temp4_y1;
  *y1 = t8 ^ temp5_y1;

  and_3(x0, x1, x3, &temp1_y2);
  and_3(x0, x2, x3, &temp2_y2);
  and_2(x0, x1, &temp3_y2);
  and_2(x0, x3, &temp4_y2);
  and_2(x1, x3, &temp5_y2);

  t23 = temp1_y2 ^ temp2_y2;
  t22 = t23 ^ temp3_y2;
  t21 = t22 ^ temp4_y2;
  t20 = t21 ^ temp5_y2;
  t19 = t20 ^ x2;
  t18 = t19 ^ x3;
  *y2 = t18 ^ 1;

  and_3(x0, x1, x2, &temp1_y3);
  and_3(x0, x1, x3, &temp2_y3);
  and_3(x0, x2, x3, &temp3_y3);
  and_2(x1, x2, &temp4_y3);

  t33 = temp1_y3 ^ temp2_y3;
  t32 = t33 ^ temp3_y3;
  t31 = t32 ^ temp4_y3;
  t30 = t31 ^ x0;
  t29 = t30 ^ x1;
  t28 = t29 ^ x3;
  *y3 = t28 ^ 1;
}


void and_2(_Bool a, _Bool b, _Bool *d)
{
  *d = a & b;
}

void and_3(_Bool a, _Bool b, _Bool c, _Bool *d)
{
  _Bool temp;
  and_2(a, b, &temp);
  and_2(temp, c, d);
}

void sbox(_Bool x0, _Bool x1, _Bool x2, _Bool x3, _Bool *y0, _Bool *y1, _Bool *y2, _Bool *y3)
{
  _Bool temp1_y0;
  _Bool temp1_y1;
  _Bool temp2_y1;
  _Bool temp3_y1;
  _Bool temp4_y1;
  _Bool temp5_y1;
  _Bool temp1_y2;
  _Bool temp2_y2;
  _Bool temp3_y2;
  _Bool temp4_y2;
  _Bool temp5_y2;
  _Bool temp1_y3;
  _Bool temp2_y3;
  _Bool temp3_y3;
  _Bool temp4_y3;
  int t1;
  int t2;
  int t8;
  int t9;
  int t10;
  int t11;
  int t12;
  int t18;
  int t19;
  int t20;
  int t21;
  int t22;
  int t23;
  int t28;
  int t29;
  int t30;
  int t31;
  int t32;
  int t33;
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


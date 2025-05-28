/* DOMAND Function Definition */
void Domand(int a0, int a1, int a2, int a3, int a4, int b0, int b1, int b2, int b3, int b4, int * c0, int * c1, int * c2, int * c3, int * c4, int r01, int r02, int r03, int r04, int r12, int r13, int r14, int r23, int r24, int r34){
		int t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19, t20, t21, t22, t23, t24;
		int i0, i1, i2, i3, i4, i5, i6, i7, i8, i9, i10, i11, i12, i13, i14, i15, i16, i17, i18, i19;

		t0 = a0 & b0;
		t1 = a0 & b1;
		i0 = t1 ^ r01;
		t2 = a0 & b2;
		i1 = t2 ^ r02;
		t3 = a0 & b3;
		i2 = t3 ^ r03;
		t4 = a0 & b4;
		i3 = t4 ^ r04;

		t5 = a1 & b0;
		i4 = t5 ^ r01;
		t6 = a1 & b1;
		t7 = a1 & b2;
		i5 = t7 ^ r12;
		t8 = a1 & b3;
		i6 = t8 ^ r13;
		t9 = a1 & b4;
		i7 = t9 ^ r14;

		t10 = a2 & b0;
		i8 = t10 ^ r02;
		t11 = a2 & b1;
		i9 = t11 ^ r12;
		t12 = a2 & b2;
		t13 = a2 & b3;
		i10 = t13 ^ r23;
		t14 = a2 & b4;
		i11 = t14 ^ r24;

		t15 = a3 & b0;
		i12 = t15 ^ r03;
		t16 = a3 & b1;
		i13 = t16 ^ r13;
		t17 = a3 & b2;
		i14 = t17 ^ r23;
		t18 = a3 & b3;
		t19 = a3 & b4;
		i15 = t19 ^ r34;

		t20 = a4 & b0;
		i16 = t20 ^ r04;
		t21 = a4 & b1;
		i17 = t21 ^ r14;
		t22 = a4 & b2;
		i18 = t22 ^ r24;
		t23 = a4 & b3;
		i19 = t23 ^ r34;
		t24 = a4 & b4;

		int t25 = 0;
		t25 = reg(i0) ^ reg(i1);
 		int t26 = 0;
		t26 = t25 ^ reg(i2);
 		int t26 = 0;
		t26 = t25 ^ reg(i3);
 		*c0 = t25 ^ t0;

 		int t26 = 0;
		t26 = reg(i4) ^ reg(i5);
 		int t27 = 0;
		t27 = t26 ^ reg(i6);
 		int t27 = 0;
		t27 = t26 ^ reg(i7);
 		*c1 = t26 ^ t6;

 		int t27 = 0;
		t27 = reg(i8) ^ reg(i9);
 		int t28 = 0;
		t28 = t27 ^ reg(i10);
 		int t28 = 0;
		t28 = t27 ^ reg(i11);
 		*c2 = t27 ^ t12;

 		int t28 = 0;
		t28 = reg(i12) ^ reg(i13);
 		int t29 = 0;
		t29 = t28 ^ reg(i14);
 		int t29 = 0;
		t29 = t28 ^ reg(i15);
 		*c3 = t28 ^ t18;

 		int t29 = 0;
		t29 = reg(i16) ^ reg(i17);
 		int t30 = 0;
		t30 = t29 ^ reg(i18);
 		int t30 = 0;
		t30 = t29 ^ reg(i19);
 		*c4 = t29 ^ t24;

 }
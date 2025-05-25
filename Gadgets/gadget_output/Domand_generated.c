/* DOMAND Function Definition */
void Domand(int a0, int a1, int a2, int b0, int b1, int b2, int * c0, int * c1, int * c2, int r01, int r02, int r12){
		int t0, t1, t2, t3, t4, t5, t6, t7, t8;
		int i0, i1, i2, i3, i4, i5;

		t0 = a0 & b0;
		t1 = a0 & b1;
		i0 = t1 ^ r01;
		t2 = a0 & b2;
		i1 = t2 ^ r02;

		t3 = a1 & b0;
		i2 = t3 ^ r01;
		t4 = a1 & b1;
		t5 = a1 & b2;
		i3 = t5 ^ r12;

		t6 = a2 & b0;
		i4 = t6 ^ r02;
		t7 = a2 & b1;
		i5 = t7 ^ r12;
		t8 = a2 & b2;

		int t9 = 0;
		t9 = reg(i0) ^ reg(i1);
 		*c0 = t9 ^ t0;

 		int t10 = 0;
		t10 = reg(i2) ^ reg(i3);
 		*c1 = t10 ^ t4;

 		int t11 = 0;
		t11 = reg(i4) ^ reg(i5);
 		*c2 = t11 ^ t8;

 }
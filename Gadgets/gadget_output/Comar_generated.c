/* COMAR Function Definition */
void Comar(int a0, int a1, int b0, int b1, int* c0, int* c1, int r0, int r1, int r_0, int r_1, int r_2, int r_3){
	int a_0;
	a_0= reg(a0 ^ r0);
	int a_1;
	a_1= reg(a1 ^ r0);
	int b_0;
	b_0= reg(b0 ^ r1);
	int b_1;
	b_1= reg(b1 ^ r1);

	int t0, t1, t2, t3;

	int c_0, c_1, c_2, c_3;
	t0 = a_0 & b_0;
	c_0 = reg(t0 ^ r_0);
	t1 = a_1 & b_0;
	c_1 = reg(t1 ^ r_1);
	t2 = a_0 & b_1;
	c_2 = reg(t2 ^ r_2);
	t3 = a_1 & b_1;
	c_3 = reg(t3 ^ r_3);
	int t4, t5;
	t4 = c_0 ^ c_1;
	t5 = t4 ^ c_2;
	*c0 = t5 ^ c_3;

	int t6, t7;

	t6 = r_0 ^ r_1;
	t7 = t6 ^ r_2;
	*c1 = reg(t7 ^ r_3);
}
struct operands {
	int a;
	int b;
	int operator;
};

program PROG {
	version VERSION {
		int ADD(operands) = 1;
		int SUB(operands) = 2;
		int MULTIPLY(operands) = 3;
		int DIVIDE(operands) = 4;
	} = 1;
} = 1111111;

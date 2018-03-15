#include "utils.h"

int calculate(Package package){
	int a = package.a;
	int b = package.b;
	char operator = package.operator;

	int result = 0;

	switch(operator){
		case '+':
			result = add(a, b);
			break;
		case '-':
			result = sub(a, b);
			break;
		case '*':
			result = multiply(a, b);
			break;
		case '/':
			result = divide(a, b);
			break;
		default:
			fprintf(stderr, "Couldn't compute result: '%c' is not a not valid operator!\n", operator);
			result = -1;
			break;
	}

	return result;
}

Package get_filled_package(){
	int a = 0;
	int b = 0;
	char operator = '@';

	printf("Insert operands and operation. Ex: 1 + 2:\n");
	scanf("%d %c %d", &a, &operator, &b);

	Package package = {a, b, operator};
	return package;
}

int add(int a, int b){
	return a + b;
}

int sub(int a, int b){
	return a - b;
}

int multiply(int a, int b){
	return a * b;
}

int divide (int a, int b){
	if(b != 0)
		return a / b;

	fprintf(stderr, "Can't divide by zero :'(\n");
	return -1;
}

/*
 * This is sample code generated by rpcgen.
 * These are only templates and you can use them
 * as a guideline for developing your own functions.
 */

#include "calculate.h"


void prog_1(char *host) {
	CLIENT *clnt;

#ifndef	DEBUG
	clnt = clnt_create (host, PROG, VERSION, "udp");
	if (clnt == NULL) {
		clnt_pcreateerror (host);
		exit(1);
	}
#endif	/* DEBUG */

	int a = 0, b = 0;
	char operator = '@';

	printf("Insert operands and operation. Ex: 1 + 2:\n");
	scanf("%d %c %d", &a, &operator, &b);

	operands operands_arg;

	operands_arg.a = a;
	operands_arg.b = b;
	operands_arg.operator = operator;

	int *result;

	switch(operator){
		case '+':
			result = add_1(&operands_arg, clnt);
			break;
		case '-':
			result = sub_1(&operands_arg, clnt);
			break;
		case '*':
			result = multiply_1(&operands_arg, clnt);
			break;
		case '/':
			result = divide_1(&operands_arg, clnt);
			break;
		default:
			fprintf(stderr, "Couldn't compute result: '%c' is not a not valid operator!\n", operator);
			result = NULL;
			break;
	}

	if (result != (int *) NULL) {
		printf("Result = %d\n", *result);
	} else {
		clnt_perror (clnt, "call failed");
	}

#ifndef	DEBUG
	clnt_destroy (clnt);
#endif	 /* DEBUG */
}


int main (int argc, char *argv[]) {
	char *host;

	if (argc < 2) {
		printf ("usage: %s server_host\n", argv[0]);
		exit (1);
	}

	host = argv[1];
	prog_1 (host);

	exit (0);
}

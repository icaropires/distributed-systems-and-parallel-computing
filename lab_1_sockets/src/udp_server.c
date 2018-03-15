#include <stdio.h>
#include "../sockets/sockets.h"
#include "../utils/utils.h"

int calculate(Package package);

int add(int a, int b);

int sub(int a, int b);

int multiply(int a, int b);

int divide(int a, int b);

int main(int argc, char *argv[]){
	if(argc == 3){
		int sfd = create_socket(AF_INET, SOCK_DGRAM, 0);
		SocketAddress server_address = get_server_address(argv[1], argv[2]);

		bind_socket(sfd, (struct sockaddr *) &server_address, sizeof(server_address));

		printf("Listening to %s:%s. Waiting for messages...\n", argv[1], argv[2]);
		while(1){
			SocketAddress client_address;

			Package package = {-1, -1, '#'};
			get_message_from(sfd, (struct sockaddr *) &client_address, sizeof(client_address), &package);

			package.result = calculate(package);

			send_message_to(sfd, &package, sizeof(Package), 0, (struct sockaddr *) &client_address, sizeof(client_address));
			printf("Result = '%d'. Package with result sended back to client!\n", package.result);
		}
	} else {
		fprintf(stderr, "Wrong format. Try: \"%s [IP] [Port]\"\n", argv[0]);
		return 1;
	}
	return 0;
}

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
	return a / b;
}

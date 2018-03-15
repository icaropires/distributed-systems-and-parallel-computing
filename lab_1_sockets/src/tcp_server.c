#include <stdio.h>
#include <signal.h>
#include "../sockets/sockets.h"


int main(int argc, char *argv[]){
	if (argc == 3){
		int sfd = create_socket(AF_INET, SOCK_STREAM, 0);
		struct sockaddr_in server_address = get_server_address(argv[1], argv[2]);

		bind_socket(sfd, (struct sockaddr *) &server_address, sizeof(server_address));
		listen_to_socket(sfd);

		while(1){
			struct sockaddr_in client_address;

			printf("Listening to %s:%s. Waiting for connections...\n", argv[1], argv[2]);
			int accepted_client = accept_client(sfd, (struct sockaddr_in *) &client_address, sizeof(client_address));

			for(int i = 4; i >= 0; --i) {
				Package package = {-1, -1, '#'};
				get_message_from_connected(accepted_client, &package, sizeof(client_address), 0);

				if(package.a != -1 && package.b != -1 && package.operator != '#') {
					package.result = calculate(package);

					send_message_to_connected(accepted_client, &package, sizeof(Package), 0);

					printf("Result = '%d'. Package with result sended back to client!\n"
						   "Client %s:%u has more %d calculations\n\n",
						   package.result, inet_ntoa(client_address.sin_addr), ntohs(client_address.sin_port), i);
				}
			}

			close(accepted_client);
			printf("Client %s:%u was disconected\n", inet_ntoa(client_address.sin_addr), ntohs(client_address.sin_port));
		}
	} else {
		fprintf(stderr, "Wrong format. Try: \"%s [IP] [Port]\"\n", argv[0]);
		return 1;
	}

	return 0;
}

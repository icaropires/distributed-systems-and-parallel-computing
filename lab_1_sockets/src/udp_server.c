#include <stdio.h>
#include "sockets.h"

int main(int argc, char *argv[]){
	if(argc == 3){
		int sfd = create_socket(AF_INET, SOCK_DGRAM, 0);
		SocketAddress server_address = get_server_address(argv[1], argv[2]);

		bind_socket(sfd, (struct sockaddr *) & server_address, sizeof(server_address));

		printf("Listening to %s:%s. Waiting for messages...\n", argv[1], argv[2]);
		while(1){
			SocketAddress client_address;

			char msg[MAX_SIZE_MSG];
			get_message_from(sfd, (struct sockaddr *) &client_address, sizeof(client_address), msg);

			printf("%s:%u said:\n%s\n", inet_ntoa(client_address.sin_addr), ntohs(client_address.sin_port), msg);
		}
	} else {
		fprintf(stderr, "Wrong format. Try: \"%s [IP] [Port]\"\n", argv[0]);
		return 1;
	}
	return 0;
}

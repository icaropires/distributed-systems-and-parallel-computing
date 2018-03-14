#include "../sockets/sockets.h"

int main(int argc, char *argv[]){
		
	if(argc == 4){
		SocketAddress client_address = get_client_address();

		SocketAddress server_address = get_server_address(argv[1], argv[2]);

		int sfd = create_socket(AF_INET, SOCK_DGRAM, 0);
		bind_socket(sfd, (struct sockaddr *) &client_address, sizeof(client_address));

		const int message_index = 3;
		send_message_to(sfd, argv[message_index], sizeof(argv[message_index]), 0, (struct sockaddr *) &server_address, sizeof(server_address));
	} else {
		fprintf(stderr, "Wrong format. Try: \"%s [IP] [Port] [Message]\"\n", argv[0]);
		return 1;
	}

	return 0;
}

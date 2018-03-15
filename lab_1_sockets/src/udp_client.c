#include "../sockets/sockets.h"
#include "../utils/utils.h"

int main(int argc, char *argv[]){
	if(argc == 3){
		int sfd = create_socket(AF_INET, SOCK_DGRAM, 0);

		struct sockaddr_in client_address = get_client_address();
		bind_socket(sfd, (struct sockaddr *) &client_address, sizeof(client_address));

		struct sockaddr_in server_address = get_server_address(argv[1], argv[2]);
		while(1){
			Package package = get_filled_package();
			send_message_to(sfd, &package, sizeof(Package), 0, (struct sockaddr *) &server_address, sizeof(server_address));
			printf("Package sent to server! Waiting for result...\n");

			get_message_from(sfd, (struct sockaddr *) &server_address, sizeof(server_address), 0, &package);
			printf("Result received! Result = '%d'!\n\n", package.result);
		}
	} else {
		fprintf(stderr, "Wrong format. Try: \"%s [IP] [Port]\"\n", argv[0]);
		return 1;
	}

	return 0;
}

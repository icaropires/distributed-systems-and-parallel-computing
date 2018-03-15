#include "../sockets/sockets.h"
#include "../utils/utils.h"

int main(int argc, char *argv[]){
	if(argc == 3){
		int sfd = create_socket(AF_INET, SOCK_STREAM, 0);
		struct sockaddr_in server_address = get_server_address(argv[1], argv[2]);

        connect_to_socket(sfd, &server_address, sizeof(server_address));

		while(1){
			Package package = get_filled_package();

			send_message_to_connected(sfd, &package, sizeof(Package), 0);
			printf("Package sent to server! Waiting for result...\n");

			get_message_from_connected(sfd, &package, sizeof(Package), 0);
			printf("Result received! Result = '%d'!\n\n", package.result);
		}
	} else {
		fprintf(stderr, "Wrong format. Try: \"%s [IP] [Port]\"\n", argv[0]);
		return 1;
	}
	return 0;
}

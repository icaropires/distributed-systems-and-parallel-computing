#include "sockets.h"

SocketAddress get_server_address(char *ip, char *port){
	SocketAddress server_address;

	server_address.sin_family = AF_INET;
	server_address.sin_addr.s_addr = inet_addr(ip);
	server_address.sin_port = htons(atoi(port));

	return server_address;
}

int create_socket(int domain, int type, int protocol){
	int sfd = socket(domain, type, protocol);

	if(sfd < 0){
		perror("Couldn't create socket.");
		exit(1);
	}

	return sfd;
}

void bind_socket(int socket, const struct sockaddr *address, socklen_t address_len){
	int error = bind(socket, address, address_len);

	if(error){
		perror("Couldn't bind socket to name.");
		exit(1);
	}
}

void get_message_from(int sfd, const struct sockaddr *address, socklen_t address_len, char* msg){
	memset(msg, 0, MAX_SIZE_MSG);

	int bytes_received = recvfrom(sfd, msg, MAX_SIZE_MSG, 0, (struct sockaddr *) address, &address_len);

	if (bytes_received == 0){
		fprintf(stderr, "No message received.\n");
	} else if (bytes_received < 0){
		perror("Couldn't receive message.");	
	}
}

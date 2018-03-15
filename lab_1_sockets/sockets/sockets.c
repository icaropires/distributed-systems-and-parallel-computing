#include "sockets.h"

SocketAddress get_server_address(char *ip, char *port){
	SocketAddress socket_address;

	socket_address.sin_family = AF_INET;
	socket_address.sin_addr.s_addr = inet_addr(ip);
	socket_address.sin_port = htons(atoi(port));

	return socket_address;
}

SocketAddress get_client_address(){
	SocketAddress socket_address;

	socket_address.sin_family = AF_INET;
	socket_address.sin_addr.s_addr = htonl(INADDR_ANY);
	socket_address.sin_port = htons(0);

	return socket_address;
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

void get_message_from(int sfd, const struct sockaddr *address, socklen_t address_len, Package *package){
	int bytes_received = recvfrom(sfd, package, sizeof(Package), 0, (struct sockaddr *) address, &address_len);

	if (bytes_received == 0){
		fprintf(stderr, "No package received.\n");
	} else if (bytes_received < 0){
		perror("Couldn't receive package.");	
	}
}

void send_message_to(int sfd, const Package *package, size_t lenght,
                     int flags, const struct sockaddr *dest_addr, socklen_t dest_len){
    int bytes_sended = sendto(sfd, package, sizeof(Package), 0, dest_addr, dest_len);

    if (bytes_sended < 0)
        perror("Couldn't send package");
}

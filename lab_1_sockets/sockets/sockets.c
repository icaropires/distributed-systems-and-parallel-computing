#include "sockets.h"

struct sockaddr_in get_server_address(char *ip, char *port){
	struct sockaddr_in socket_address;

	socket_address.sin_family = AF_INET;
	socket_address.sin_addr.s_addr = inet_addr(ip);
	socket_address.sin_port = htons(atoi(port));

	return socket_address;
}

struct sockaddr_in get_client_address(){
	struct sockaddr_in socket_address;

	socket_address.sin_family = AF_INET;
	socket_address.sin_addr.s_addr = htonl(INADDR_ANY);
	socket_address.sin_port = htons(0);

	return socket_address;
}

int create_socket(int domain, int type, int protocol){
	int sfd = socket(domain, type, protocol);

	if(sfd < 0){
		perror("Couldn't create socket");
		exit(1);
	}

	return sfd;
}

void bind_socket(int socket, const struct sockaddr *address, socklen_t address_len){
	int error = bind(socket, address, address_len);

	if(error){
		perror("Couldn't bind socket to name");
		exit(1);
	}
}

void get_message_from(int sfd, const struct sockaddr *address, socklen_t address_len, int flags, Package *package){
	int bytes_received = recvfrom(sfd, package, sizeof(Package), flags, (struct sockaddr *) address, &address_len);

	if (bytes_received == 0){
		fprintf(stderr, "No package received.\n");
	} else if (bytes_received < 0){
		perror("Couldn't receive package");	
	}
}

void send_message_to(int sfd, const Package *package, size_t lenght,
                     int flags, const struct sockaddr *dest_addr, socklen_t dest_len){
    int bytes_sended = sendto(sfd, package, sizeof(Package), 0, dest_addr, dest_len);

    if (bytes_sended < 0)
        perror("Couldn't send package");
}

void send_message_to_connected(int sfd, const Package *package, size_t lenght, int flags){
    int bytes_sended = send(sfd, package, lenght, flags);

    if (bytes_sended < 0)
        perror("Couldn't send package");
}

void listen_to_socket(int sfd) {
    if (listen(sfd, QUEUE_LENGHT) < 0) {
        perror("Couldn't start listening to socket");
        exit(1);
    }
}

void connect_to_socket(int sfd, const struct sockaddr_in *server_address, socklen_t address_len){
    if (connect(sfd, (const struct sockaddr *) server_address, address_len) < 0) {
        perror("Couldn't connect with server");
        exit(1);
    }
}

int accept_client(int sfd, struct sockaddr_in *client_address, socklen_t address_len){
    int accepted_client = accept(sfd, (struct sockaddr *) client_address, &address_len);

    if (accepted_client >= 0){
        printf("Client %s:%u connected\n", inet_ntoa(client_address->sin_addr), ntohs(client_address->sin_port));
    } else {
        perror("Couldn't accept client");
        exit(1);
    }

    return accepted_client;
}

void get_message_from_connected(int sfd, Package *package, size_t lenght, int flags){
	int bytes_received = recv(sfd, package, sizeof(Package), flags);

	if (bytes_received < 0){
		perror("Couldn't receive package");	
	}
}

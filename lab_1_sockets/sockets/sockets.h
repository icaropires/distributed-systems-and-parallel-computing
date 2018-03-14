#ifndef SOCKETS_H_
#define SOCKETS_H_

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>

#define MAX_SIZE_MSG 100

typedef struct sockaddr_in SocketAddress;

SocketAddress get_server_address();

int create_socket(int domain, int type, int protocol);

void bind_socket(int socket, const struct sockaddr *address, socklen_t address_len);

void get_message_from(int sfd, const struct sockaddr *address, socklen_t address_len, char *msg);


#endif  // SOCKETS_H_

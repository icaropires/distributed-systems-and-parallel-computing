#ifndef SOCKETS_H_
#define SOCKETS_H_

#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include "../utils/utils.h"

#define QUEUE_LENGHT 5

struct sockaddr_in get_server_address(char *ip, char *port);

struct sockaddr_in get_client_address();

int create_socket(int domain, int type, int protocol);

void bind_socket(int socket, const struct sockaddr *address, socklen_t address_len);

void get_message_from(int sfd, const struct sockaddr *address, socklen_t address_len, int flags, Package *package);

void send_message_to(int sfd, const Package *package, size_t lenght, int flags, const struct sockaddr *dest_addr, socklen_t dest_len);

void send_message_to_connected(int sfd, const Package *package, size_t lenght, int flags);

void listen_to_socket(int sfd);

void connect_to_socket(int sfd, const struct sockaddr_in *server_address, socklen_t address_len);

int accept_client(int sfd, struct sockaddr_in *client_address, socklen_t address_len);

void get_message_from_connected(int sfd, Package *package, size_t lenght, int flags);

#endif  // SOCKETS_H_

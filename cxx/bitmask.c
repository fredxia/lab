#include <stdio.h>
#include <stdint.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

int main()
{
  for (int i = 0; i < 32; i++) {
    uint32_t mask = 0xFFFFFFFF << (32 - i);
    struct in_addr addr = {s_addr : htonl(mask)};
    printf("%d: %x, %s\n", i, mask, inet_ntoa(addr));
  }
}

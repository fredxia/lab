
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include <assert.h>
#include <netinet/in.h>
#include <arpa/inet.h>

int main(int argc, char** argv)
{
  const char* ipStr = argv[1];
  struct sockaddr_in ipAddr;
  memset(&ipAddr, 0, sizeof(ipAddr));
  ipAddr.sin_family = AF_INET;
//  ipAddr.sin_family = AF_UNSPEC;
  ipAddr.sin_addr.s_addr = inet_addr(ipStr);
//  assert(ipAddr.sin_addr.s_addr != INADDR_NONE);
  ipAddr.sin_port = 0;
  char hostBuf[NI_MAXHOST];

  printf("size is %d\n", sizeof(sockaddr_in));
  
  int r;
  if ((r = getnameinfo((struct sockaddr*)&ipAddr, sizeof(ipAddr),
                       hostBuf, sizeof(hostBuf),
                       NULL, 0, NI_NAMEREQD)) == 0) {
    printf("host is %s\n", hostBuf);
  } else {
    printf("Cannot resolve %s: %s\n", ipStr,
           gai_strerror(r));
  }
  printf("done\n");
}

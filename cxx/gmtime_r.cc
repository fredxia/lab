#include <time.h>
#include <stdio.h>

int main()
{
  time_t t = time(0);
  struct tm gmTime;
  gmtime_r(&t, &gmTime);
  char buf[64];
  strftime(buf, sizeof(buf), "%F %T", &gmTime);
  printf("%s\n", buf);
}

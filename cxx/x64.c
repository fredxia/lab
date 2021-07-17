#include <stdint.h>
#include <stdio.h>

int64_t
x_read_base_64(const char *s)
{
  int64_t u = 0;
  while (*s!= 0)
    {
      const char c = *s++;
      int64_t b = 0; // semi-stupid compiler
      if (c>='a')
	b = c - 'a' + 26;
      else if (c>='A')
	b = c - 'A' + 0;
      else if (c>='0')
	b = c - '0' + 52;
      else if (c=='+')
	b = 62;
      else if (c=='/')
	b = 63;
      u = (u << 6) + b;
    }
  return u;
}

int main()
{
  const char* t[] = {
    "IAA",
    "Q",
    "BA",
    "AA",
    "BAAAAC",
    "QAIAA",
    "ggAAA",
    0
  };
  int i;
  for (i = 0; t[i]; i++) {
    int64_t a = x_read_base_64(t[i]);
    printf("%s => %8.8lx\n", t[i], a);
  }
}


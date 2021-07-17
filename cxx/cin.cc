#include <stdlib.h>
#include <stdio.h>
#include <iostream>
#include <time.h>
#include <unistd.h>

using namespace std;

uint64_t clock_time_diff(const struct timespec& earlier,
                                   const struct timespec& later)
{
  return (uint64_t)(((later.tv_sec + later.tv_nsec * 1e-9) -
                     (earlier.tv_sec + earlier.tv_nsec * 1e-9)) * 1000);
}


int main()
{
  int a, b;
//  cin >> a >> b;
//  cout << a << "," << b << endl;
  uint64_t abc = 0;
  double xxx = 123.223321;
  abc = (uint64_t)xxx;
  printf("%lf, %d\n", xxx, abc);

  struct timespec one;
  clock_gettime(CLOCK_REALTIME, &one);
  sleep(1);
  struct timespec two;
  clock_gettime(CLOCK_REALTIME, &two);
  abc = clock_time_diff(one, two);
  cout << abc << endl;
}

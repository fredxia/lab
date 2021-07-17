#include <stdio.h>
#include <string.h>
#include <map>

using namespace std;

enum ABC {
  A1,
  A2,
  A_end
};

enum XYZ {
  X1,
  X2,
  X_end
};

template<typename EnumClass, size_t EnumEnd>
struct Counters {
  void increment_counter(EnumClass e) {
    counters[e]++;
  }
  map<int, int> map_counters;
  int counters[EnumEnd];
};

typedef struct Counters<ABC, A_end> ACounters;
typedef struct Counters<XYZ, X_end> XCounters;

int main()
{
  ACounters acounters;
  XCounters xcounters;
  xcounters.increment_counter(X1);
  acounters.increment_counter(A1);
  return 0;
}

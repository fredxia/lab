#include <utility>
#include <algorithm>
#include <iostream>
#include <vector>
#include <map>
#include <string.h>

int main()
{
  static const std::vector<const char*> values{"a", "b", "c", "d"};
  int c = std::any_of(values.begin(), values.end(),
                      [](const char* v) { return strcmp(v, "a") != 0; });
  std::cout <<  c << std::endl;

  // braced initializer trick
  static const std::map<int, std::pair<const char*, const char*>>
    tags{ {1, {"2", "3"} }, {2, {"3", "4"} } };

  std::map<int, int> a1;
  std::map<int, int> b1;
  
  a1[1] = 2;
  a1[3] = 4;
  b1 = a1;
  std::cout << b1[3] << std::endl;
  int ai[3]{1,2,3};
  int bi[3];
  bi = ai;
  std::cout << bi[2] << std::endl;
}

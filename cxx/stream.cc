#include <iostream>
#include <sstream>
#include <algorithm>
#include <vector>
#include <memory>
#include <time.h>

enum CharType {
  Wake_Up = 'a',
  Do_Something = 'b'
};

const char* customers[][2] = {
  { "a", "b" },
  { "c", "d" },
  { "d", "d" }
};

struct A {
  int a;
  A(int v) : a(v) {}
};

typedef std::unique_ptr<A> A_ptr;

int main()
{
  std::ostringstream oss;
  oss << "1234 " << 1234;
  std::string a = oss.str();
  std::cout << a << std::endl;

  std::vector<A_ptr> ptr_coll;
  A_ptr aptr = std::unique_ptr<A>(new A(2));
  ptr_coll.push_back(std::move(aptr));

  time_t timestamp = time(0);
  std::string abcde = "abcde";

  auto my_func = [timestamp, abcde](const char* xyz) {
    char buffer[32];    
    std::string a = abcde;
    snprintf(buffer, sizeof(buffer), "%ld", timestamp);
    a += buffer;
    return a + xyz;
  };

  std::cout << my_func("dddd") << std::endl;
  
  try {
    throw std::string("abcde");
  } catch (std::string x) {
    std::cout << x << std::endl;
  }
  std::vector<int> values;
  for (int i = 0; i < 20; i++) {
    values.push_back(i * 10);
  }
  int val = 19;
  std::vector<int>::reverse_iterator lower =
    std::lower_bound(values.rbegin(), values.rend(), val,
                     [](int a, int b){ return a > b;});
  std::vector<int>::iterator upper = std::upper_bound(values.begin(), values.end(), val);
  std::cout << "lower " << *lower << " upper " << *upper << std::endl;

}

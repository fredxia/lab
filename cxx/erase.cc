#include <set>
#include <string>
#include <stdio.h>

using namespace std;

int main()
{
  char buffer[32];
  set<string> values;
  for (int i = 0; i < 100; i++) {
    snprintf(buffer, sizeof(buffer), "%2.2d", i);
    values.insert(buffer);
  }
  auto it = values.begin();
  while (it != values.end()) {
    if (it->c_str()[it->length()-1] == '0' ||
        it->c_str()[it->length()-1] == '5') {
//      set<string>::iterator it2 = it;
//      it2++;
      values.erase(it);
      it++;
//      it = it2;
    } else {
      it++;
    }
  }
  for (it = values.begin(); it != values.end(); it++) {
    printf("%s\n", it->c_str());
  }

  string abc = "abc";
  abc += std::to_string(20);
  printf("%s\n", abc.c_str());
  return 0;
}

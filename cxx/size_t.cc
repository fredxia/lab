#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <unordered_map>


inline size_t hash_const_char(const char* const& s)
{
  return ((unsigned long)(s));
}

struct hash_cstr {
  size_t operator()(const char* const& s) const noexcept {
    return ((unsigned long)(s));
  }
};

struct equal_cstr {
  bool operator ()(const char* const& s1,
                   const char* const& s2) const noexcept {
    return s1 == s2;
  }
};

inline bool equal_const_char(const char* const& s1,
                             const char* const& s2)
{
  return s1 == s2;
}

typedef std::unordered_map< const char*, unsigned long,
                            hash_cstr, equal_cstr> hash_table;

int main()
{
  size_t v1 = hash_const_char("abcd");
  size_t v2 = hash_const_char("xyz");
  printf("%lx, %lx\n", v1, v2);

  hash_table table;
  table["abcd"] = 10;
  table["xyz"] = 20;
}

#include <string>
#include <iostream>

int main()
{
  std::string abcd("https://abcd.com");
  std::string xyz("http://abcd.com");

  std::cout << sizeof("https://") << std::endl;
  
  if (abcd.substr(0, sizeof("https://") - 1) == "https://") {
    std::cout << "yes" << std::endl;
  }
  if (xyz.substr(0, sizeof("https://") - 1) == "https://") {
    std::cout << "yes" << std::endl;
  }

}

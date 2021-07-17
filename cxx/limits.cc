#include <limits>
#include <iostream>

using namespace std;
int main()
{
  cout << "unsigned int max: " << std::hex
       << std::numeric_limits<unsigned int>::max()
       << " min: " << std::numeric_limits<unsigned int>::min() << endl;

  cout << "int max: " << std::hex
       << std::numeric_limits<int>::max() << std::dec
       << " min: " << std::numeric_limits<int>::min()
       << "min hex: " << std::hex << std::numeric_limits<int>::min() << endl;

  cout << "neg int 0xFFFFFFFF " << std::dec << (int)(0xFFFFFFFF) << endl;
  cout << "neg hex -2 " << std::hex << (int)(-2) << endl;
  cout << "neg int 0x80000000 " << std::dec << (int)(0x80000000) << endl;
  cout << "positive int 0x7FFFFFFF " << std::dec << (int)(0x7FFFFFFF) << endl;
  
  cout << "neg int 0x80000001 " << std::dec << (int)(0x80000001) << endl;
  cout << "neg int 0x80000010 " << std::dec << (int)(0x80000010) << endl;
  
  cout << "unsigned long max: " << std::hex
       << std::numeric_limits<unsigned long>::max()
       << " min: " << std::numeric_limits<unsigned long>::min() << endl;
}

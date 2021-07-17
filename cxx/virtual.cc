#include <iostream>

struct Virtual {
  virtual int abc(int v) = 0;
  virtual int xyz(int v);
};

struct ABC : public Virtual {
  virtual int abc(int v) {
    return 10 + v;
  }
  virtual int xyz(int v) {
    return 20 + v;
  }
};

int main()
{
  ABC a;
  std::cout << a.abc(5) << "," << a.xyz(10) << std::endl;
}



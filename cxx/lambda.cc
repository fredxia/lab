#include <iostream>
#include <string>

using namespace std;

struct A {
  int a;
  A(int v) : a(v) {}
};

int main()
{
  A abc(10);
  auto func = [abc](int x) mutable { abc.a = x; return 0; };
  func(20);
  cout << abc.a << endl;
}


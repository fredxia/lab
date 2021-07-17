#include <iostream>
#include <utility>
#include <memory>
#include "graph.h"

struct A {
  A(int a) : v(a) {}
  int v;
};

typedef std::shared_ptr<A> A_sp;

int main()
{
    // Edge* a = new Edge("abcd", "xyz", 20);
    // EdgePtr ptr(a);
    // EdgePtrCollection coll;

    // // a moved from ptr into vector coll. ptr now is empty
    // coll.push_back(std::move(ptr));

    // std::cout << "ptr: " << ptr.get() << std::endl;
    // std::cout << "vector: " << coll[0].get() << std::endl;

    char* abcd = (char*)"ssdd";
    std::cout << (void*)abcd << std::endl;    
    std::string d(std::move(abcd));
    std::cout << (void*)d.c_str() << std::endl;
    std::cout << (void*)abcd << std::endl;

    A_sp aptr(new A(10));
    std::cout << aptr->v << std::endl;
}

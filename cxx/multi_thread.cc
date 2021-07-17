#include <thread>
#include <iostream>
#include <atomic>

using namespace std;

struct Thread {
  atomic<bool> paused;
  
  int run()
};

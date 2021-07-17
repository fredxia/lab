
#include <stdint.h>
#include <time.h>
#include <string.h>
#include <string>
#include <thread>
#include <iostream>
#include <map>
#include <memory>
#include <chrono>
#include <boost/lockfree/spsc_queue.hpp>

using namespace std;

enum counter_type {
  counter_success,
  counter_failure,
  counter_large,
  counter_small,
  counter_end
};

enum worker_instruction {
  instruction_exit,
  instruction_copy_counters,
  instruction_end
};

typedef uint64_t counter_values[counter_end];

static counter_values my_counters;

struct counter_set {
  uint64_t counters[counter_end];
};

typedef boost::lockfree::spsc_queue<uint32_t> channel_main_to_worker;
typedef boost::lockfree::spsc_queue<counter_set> channel_worker_to_main;

//template<typename T> std::map<T, uint64_t> Distribution;
template<typename T>
using channel = boost::lockfree::spsc_queue<T>;

struct worker {
  uint32_t sleep_interval;
  counter_set my_counters;
  channel_main_to_worker to_worker;
  channel_worker_to_main to_main;

  worker(uint32_t interval)
    : sleep_interval(interval), to_worker(1), to_main(1) {
    memset(&my_counters, 0, sizeof(my_counters));
  }

  void run() {
    uint32_t instruction;
    while (true) {
      if (to_worker.pop(instruction)) {
        switch (instruction) {
        case instruction_exit:
          cout << "exit thread: " << std::this_thread::get_id() << endl;
          return;
        case instruction_copy_counters:
          to_main.push(my_counters);
          break;
        default:
          return;
        }
      }
      std::this_thread::sleep_for(std::chrono::milliseconds(sleep_interval));
      for (uint32_t c = counter_success; c < counter_end; c++) {
        my_counters.counters[c]++;
      }
    }
  }
};

typedef unique_ptr<worker> worker_ptr;
typedef unique_ptr<std::thread> thread_ptr;

static map<thread_ptr, worker_ptr> thread_collection;

void worker_func(worker* worker_instance)
{
  worker_instance->run();
}

int main(int argc, char** argv)
{
  counter_set main_counters;
  uint32_t num_threads;
  
  if (argc > 2) {
    num_threads = atoi(argv[1]);
  } else {
    num_threads = 1024;
  }

  cout << "size: " << sizeof(my_counters) << endl;
  
  memset(&main_counters, 0, sizeof(main_counters));
  
  for (uint32_t i = 0; i < num_threads; i++) {
    uint32_t interval = ((i % 4) + 1) * 1000;
    worker* wk = new worker(interval);
    std::thread* thr = new std::thread(worker_func, wk);
    thread_collection[thread_ptr(thr)] = worker_ptr(wk);
  }

  for (auto& it : thread_collection) {
    cout << it.first->get_id() << endl;
  }

  time_t start_time = time(0);
  while (true) {
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));
    for (auto i = thread_collection.begin(); i != thread_collection.end();
         i++) {
      if (!i->second->to_worker.push(instruction_copy_counters)) {
        cout << "thread instruction " << i->first->get_id() << " full" << endl;
      }
    }
    std::this_thread::sleep_for(std::chrono::milliseconds(1000));
    counter_set counters_from_thread;
    for (auto i = thread_collection.begin(); i != thread_collection.end();
         i++) {
      memset(&counters_from_thread, 0, sizeof(counters_from_thread));
      if (!i->second->to_main.pop(counters_from_thread)) {
        cout << "thread " << i->first->get_id() << "did not fill counters"
             << endl;
      } else {
        // cout << "received counters from thread "
        //      << i->first->get_id() << "," << i->second->sleep_interval << " : ";
        for (uint32_t c = counter_success; c != counter_end; c++) {
          cout << counters_from_thread.counters[c];
          cout << ",";
        }
        cout << endl;
      }
      for (uint32_t c = counter_success; c < counter_end; c++) {
        main_counters.counters[c] += counters_from_thread.counters[c];
      }
    }
    for (uint32_t c = counter_success; c < counter_end; c++) {
      cout << c << " : " << main_counters.counters[c] << endl;
    }
    time_t cur = time(0);
    if (cur - start_time > 30) {
      // Give worker thread a bit time to empty instructions
      std::this_thread::sleep_for(std::chrono::milliseconds(1000));
      cout << "exiting... " << endl;
      for (auto i = thread_collection.begin(); i != thread_collection.end();
           i++) {
        if (!i->second->to_worker.push(instruction_exit)) {
          cout << "thread exit fail " << i->first->get_id() << endl;
        }
      }
      std::this_thread::sleep_for(std::chrono::milliseconds(1000));
      for (auto i = thread_collection.begin(); i != thread_collection.end();
           i++) {
        auto thread_id = i->first->get_id();
        i->first->join();
        cout << "thread exited: " << thread_id << endl;
      }
      cout << "All threads exit" << endl;
      break;
    }
    my_counters[0] = counters_from_thread.counters[0];
  }
}


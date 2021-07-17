#include <pthread.h>
#include <stdio.h>
#include <time.h>
#include <string.h>
#include <stdlib.h>
#include <atomic>

struct atomic_stuff {
  std::atomic_int atomics[100];
};

struct regular_stuff {
  int values[100];
};
 
static int num_loops;
static int num_threads;

void* update_atomic(void* arg)
{
//  printf("In update_atomic\n");
  int v;
  atomic_stuff* stuff = (atomic_stuff*)arg;
  for (int i = 0; i < num_loops; i++) {
    for (int j = 0; j < 100; j++) {
      stuff->atomics[j].store(i + j);
      v = stuff->atomics[j].load();      
    }
//    printf("atomic %i\n", i);
  }
  delete stuff;
  return nullptr;
}

void* update_func(void* arg)
{
//  printf("In update_func\n");
  int v;
  regular_stuff* stuff = (regular_stuff*)arg;
  for (int i = 0; i < num_loops; i++) {
    for (int j = 0; j < 100; j++) {
      stuff->values[j] = i + j;
      v = stuff->values[j];
    }
//    printf("regular %i\n", i);    
  }
  delete stuff;
  return nullptr;
}


int main(int argc, char** argv)
{
  struct timespec start_time, end_time;

  int num_threads = atoi(argv[1]);
  int num_loops = atoi(argv[2]);
  const char* mode = argv[3];
  
  pthread_t threads[num_threads];

  printf("Num threads %d, loops %d, mode %s\n",
         num_threads, num_loops, mode);
  
  clock_gettime(CLOCK_MONOTONIC, &start_time);
  if (mode[0] == 'a') {
    for (int i = 0; i < num_threads; i++) {
      auto stuff = new atomic_stuff;
      pthread_create(&threads[i], nullptr, update_atomic, stuff);
    }
  } else {
    for (int i = 0; i < num_threads; i++) {
      auto stuff = new regular_stuff;
      pthread_create(&threads[i], nullptr, update_func, stuff);
    }
  }
  for (int i = 0; i < num_threads; i++) {
    pthread_join(threads[i], nullptr);
  }
  clock_gettime(CLOCK_MONOTONIC, &end_time);

  double start_double = start_time.tv_sec + start_time.tv_nsec * 1e-9;
  double end_double = end_time.tv_sec + end_time.tv_nsec * 1e-9;
  printf("%lf\n", end_double - start_double);
}

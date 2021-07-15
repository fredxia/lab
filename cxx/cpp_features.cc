//
// Some useful c++ feature snippets
//
#include <assert.h>
#include <string.h>
#include <iostream>
#include <algorithm>
#include <vector>
#include <map>
#include <utility>
#include <fstream>
#include <memory>

using namespace std;

//
// Sorting a vector with lambda function
//
typedef pair<int, int> vec_value;
void sort_a_vector()
{
  // sort int array
  int arr[]{ 2, 3, 1, 5, 9, 10, 21, 0, 22, 0 };
  auto my_func = [](int a, int b) {
    return a < b;
  };
  size_t sz = sizeof(arr) / sizeof(int);
  // the end must be the address over the last element
  std::sort(&arr[0], &arr[sz], my_func);
  for (size_t i = 0; i < sz-1; i++) {
    assert(arr[i] <= arr[i+1]);
  }
  for (size_t i = 0; i < sz; i++) {
    cout << arr[i] << endl;
  }

  // sort vector of pairs by first element
  vector<vec_value> values{{12, 3}, {3, 5}, {10, 1}, {4, 20}, {5, 0}};
  auto vec_sort = [](const vec_value& a, const vec_value& b) {
    return a.first < b.first;
  };
  std::sort(values.begin(), values.end(), vec_sort);
  for (size_t i = 0; i < values.size() - 1; i++) {
    assert(values[i].first < values[i+1].first);
  }
  for (auto v : values) {
    cout << "(" << v.first << ", " << v.second << ")" << endl;
  }
}

//
// C++ any_of algorithm
//
void any_of_value()
{
  vector<const char*> values{"a", "b", "c", "d", "c"};
  auto c = std::any_of(values.begin(), values.end(),
                       [](const char* v) { return strcmp(v, "c") == 0; });
  assert(c == true);
  c = std::any_of(values.begin(), values.end(),
                  [](const char* v) { return strcmp(v, "x") == 0; });
  assert(c == false);
}

//
// Basic C++ functions
//
struct MyObject {
  MyObject(const char* v) {
    value = strdup(v);
  }
  ~MyObject() {
    cout << "Delete my object" << endl;
    free(value);
    value = nullptr;
  }
  char* value;
};

typedef shared_ptr<MyObject> MyObject_sp;

void basic_functions()
{
  string abc = "abc";
  abc += std::to_string(100); // std::to_string
  assert(abc == "abc100");

  char* p = 0;
  static_assert(sizeof(p) == 8, "Failed");

  // only const can static_assert value
  const int a = 2000;
  static_assert(a == 2000, "Failed");

  // fstream
  ifstream my_file;
  my_file.open("../sample/abcd.txt");
  int n, m;
  string ss;
  my_file >> n >> m >> ss;
  cout << "n: " << n << " m: " << m << " str: " << ss << endl;

  // shared_ptr
  MyObject_sp obj_ptr(new MyObject("abcdefg"));
  {
    MyObject_sp obj2 = obj_ptr;
  }
  cout << (obj_ptr == nullptr ? "NULL" : "Not NULL")
       << " value: " << obj_ptr->value << endl;
  MyObject_sp obj_ptr2;
  cout << "empty obj_ptr2 "
       << (obj_ptr == NULL ? "NULL" : "Not NULL")
       << " object " << obj_ptr2.get()
       << endl;
}

//
// Limits
//
void show_numeric_limits()
{
  // std::hex and std::dec formatters
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

struct Deleter {
  void operator() (MyObject* obj) {
    cout << "Calling deleter on obj: " << obj->value << endl;
    delete obj;
  }
};

void unique_ptr_with_deleter()
{
  std::unique_ptr<MyObject, Deleter> my_ptr(new MyObject("abcde"));
}

int main()
{
  sort_a_vector();
  any_of_value();
  basic_functions();
  show_numeric_limits();
  unique_ptr_with_deleter();
}

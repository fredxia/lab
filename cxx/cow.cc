#include <stdio.h>
#include <string.h>
#include <assert.h>
#include <string>
#include <vector>
#include <algorithm>
#include <iostream>
#include <fstream>

using namespace std;

struct walk_stop {
  int x;
  int y;
  int extra_walk;

  walk_stop(int i, int x, int y) : x(x), y(y), extra_walk(0) {}
};

bool sort_position(const walk_stop& s1, const walk_stop& s2)
{
  return s1.extra_walk > s2.extra_walk;
};

int main(int argc, char** argv)
{
  ifstream myfile;
  myfile.open(argv[1]);

  int N, K;
  myfile >> N;
  myfile >> K;

//  cout << "N " << N << " K " << K << endl;

  vector<walk_stop> stops;
  int i, x, y;
  for (i = 0; i < N; i++) {
    myfile >> x;
    myfile >> y;
    stops.push_back(walk_stop(i, x, y));
  }
  myfile.close();

  // Initial, best distance
  int distance = abs(stops[N-1].x - stops[0].x) + abs(stops[N-1].y - stops[0].y);
//  cout << "dist " << distance << endl;
  
  for (i = 1; i < N; i++) {
    int distPrevToDest = abs(stops[i-1].x - stops[N-1].x) + abs(stops[i-1].y - stops[N-1].y);
    int distPrevToStop = abs(stops[i-1].x - stops[i].x) + abs(stops[i-1].y - stops[i].y);
    int distStopToDest = abs(stops[i].x - stops[N-1].x) + abs(stops[i].y - stops[N-1].y);
    int c = (distPrevToStop + distStopToDest - distPrevToDest);
    stops[i].extra_walk = c;
  }

  sort(stops.begin(), stops.end(), sort_position);

  for (int i = 0; i < K; i++) {
    stops[i].extra_walk = 0; // skip the stop
//    cout << "skip " << stops[i].x << ", " << stops[i].y << endl;
  }
  for (; i < N; i++ ) {
    if (stops[i].extra_walk > 0) {
//      cout << " add " << i << " " << stops[i].extra_walk << endl;
      distance += stops[i].extra_walk;
    }
  }
  cout << distance << endl;
}

#include <map>
#include <string>
#include <set>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

using namespace std;

typedef pair<int, int> Coordinate;
typedef pair<int, int> Sums;
typedef set<int> LinePoints;

int main(int argc, char** argv)
{
  // (x, y) => (sumX, sumY)
  map< Coordinate, Sums > xySums;

  // x => y points along a vertical line
  map< int, LinePoints > yPoints;
  
  // y => x points along a horizontal line
  map< int, LinePoints > xPoints;

  FILE* fh = fopen(argv[1], "r");
  char buffer[200];
  while (fgets(buffer, sizeof(buffer), fh)) {
    buffer[strlen(buffer) - 1] = 0;
    char* p = index(buffer, ' ');
    *p++ = 0;
    int newX = atoi(buffer);
    int newY = atoi(p);

    // For every existing point y on the vertial line of newX, the sumY of
    // (newX, y) => (sumX, sumY) should be incremented by abs(y - newY)
    auto yIter = yPoints.find(newX);
    if (yIter != yPoints.end()) {
      LinePoints& verticalLine(yIter->second);
      for (auto it = verticalLine.begin(); it != verticalLine.end(); it++) {
        int y = (*it);
        Coordinate xy(newX, y);
        auto sumIter = xySums.find(xy);
        // sumInter.second is Sums
        sumIter->second.second += abs(y - newY);
      }
    }

    // For every existing point x on horizontal line of newY, the sumX of
    // (x, newY) => (sumX, sumY) should be incremented by abs(x - newX)
    auto xIter = xPoints.find(newY);
    if(xIter != xPoints.end()) {
      LinePoints& horizontalLine(xIter->second);
      for (auto it = horizontalLine.begin(); it != horizontalLine.end(); it++) {
        int x = (*it);
        Coordinate xy(x, newY);
        auto sumIter = xySums.find(xy);
        sumIter->second.first += abs(x - newX);
      }
    }
    
    yPoints[newX].insert(newY);
    xPoints[newY].insert(newX);
    xySums[Coordinate(newX, newY)] = Sums(0, 0);
  }
  fclose(fh);

  float total = 0;
  for (auto it = xySums.begin(); it != xySums.end(); it++) {
    total += (float)it->second.first * (float)it->second.second / 2.0;
  }
  printf("%f\n", total);
  return 0;
}

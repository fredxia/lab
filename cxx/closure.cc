//
// Compute DAG closure
//
#include <string>
#include <set>
#include <map>
#include <iostream>
#include <assert.h>
#include "graph.h"


using namespace std;

int main(int argc, char** argv)
{
    EdgeCollection edges;
    if (!loadGraph(argv[1], edges)) {
        exit(1);
    }

    size_t sz = edges.size();
    assert(sz > 0);

    // map node name to metric colume/row number
    size_t idx = 0;
    map<string, size_t> nodes;
    map<size_t, string> nodesx;
    for (auto & e : edges) {
        cout << e.fromNode << "->" << e.toNode << endl;
        if (nodes.find(e.fromNode) == nodes.end()) {
            nodes[e.fromNode] = idx;
            nodesx[idx] = e.fromNode;
            idx++;
        }
        if (nodes.find(e.toNode) == nodes.end()) {
            nodes[e.toNode] = idx;
            nodesx[idx] = e.toNode;
            idx++;
        }
    }

    sz = nodes.size();
    bool metric[sz][sz];
    size_t i, j, k;

    // Initialize the metric. Graph is a DAG. Only need half metric.
    for (i = 0; i < sz; i++) {
        for (j = 0; j < sz; j++) {
            metric[i][j] = false;
        }
    }
    for (auto e : edges) {
        i = nodes[e.fromNode];
        j = nodes[e.toNode];
        metric[i][j] = true;
    }

    // perform the FW algorithm
    for (k = 0; k < sz; k++) {
        for (i = 0; i < sz; i++) {
            for (j = 0; j < sz; j++) {
                if (metric[i][j] == false) {
                    if (metric[i][k] == true and metric[k][j] == true) {
                        metric[i][j] = true;
                    }
                }
            }
        }
    }

    // print result
    cout << "closure:" << endl;
    for (auto n : nodes) {
        cout << n.first << ":" << endl;
        cout << "\t";
        i = n.second;
        for (j = 0; j < sz; j++) {
            if (metric[i][j] == true) {
                cout << nodesx[j] << ",";
            }
        }
        cout << endl;
    }
    exit(0);
}

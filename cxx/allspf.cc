//
// Compute all-node SPF
//
#include <assert.h>
#include <string>
#include <set>
#include <map>
#include <iostream>
#include <boost/multi_array.hpp>
#include "graph.h"

using namespace std;

static const unsigned int maxCost = 0x0FFFFFFF;
static const unsigned int directReach = 0x0FFFFFF;
static const unsigned int noReach = 0x01FFFFFF;

typedef boost::multi_array<unsigned int, 2> EdgeMetric;
static bool getPath(const map<size_t, string>& idxToNode,
                    const EdgeMetric& pathIdxs,
                    size_t fromIdx,
                    size_t toIdx,
                    vector<string>& result)
{
    size_t middle = pathIdxs[fromIdx][toIdx];    
    if (middle == noReach) {
        return false;
    }
    if (middle == directReach) {
        auto it = idxToNode.find(fromIdx);
        assert(it != idxToNode.end());
        result.push_back(it->second);
        it = idxToNode.find(toIdx);
        assert(it != idxToNode.end());
        result.push_back(it->second);
        return true;
    }
    vector<string> toMiddle;
    vector<string> middleTo;
    getPath(idxToNode, pathIdxs, fromIdx, middle, toMiddle);
    getPath(idxToNode, pathIdxs, middle, toIdx, middleTo);
    for (auto & p : toMiddle) {
        result.push_back(p);
    }
    middleTo.erase(middleTo.begin());
    for (auto & p : middleTo) {
        result.push_back(p);
    }
    return true;
}

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

    EdgeMetric costMetric(boost::extents[sz][sz]);
    EdgeMetric reachMetric(boost::extents[sz][sz]);
    
    size_t i, j, k;

    // Initialize the metric. Graph is a DAG. Only need half metric.
    for (i = 0; i < sz; i++) {
        for (j = 0; j < sz; j++) {
            costMetric[i][j] = maxCost;
            reachMetric[i][j] = noReach;
        }
    }
    for (auto e : edges) {
        i = nodes[e.fromNode];
        j = nodes[e.toNode];
        costMetric[i][j] = e.cost;
        reachMetric[i][j] = directReach;
    }

    unsigned int cost;
    for (k = 0; k < sz; k++) {
        for (i = 0; i < sz; i++) {
            for (j = 0; j < sz; j++) {
                if (costMetric[i][k] < maxCost &&
                    costMetric[k][j] < maxCost) {
                    cost = costMetric[i][k] + costMetric[k][j];
                    if (cost < costMetric[i][j]) {
                        costMetric[i][j] = cost;
                        reachMetric[i][j] = k;
                    }
                }
            }
        }
    }

    for (i = 0; i < sz; i++) {
        for (j = 0; j < sz; j++) {
            if (i == j) {
                continue;
            }
            vector<string> path;
            if(!getPath(nodesx, reachMetric, i, j, path)) {
                // cout << "No reach from " << nodesx[i]
                //      << " to " << nodesx[j] << endl;
            } else {
                for (auto v : path) {
                    cout << v << ", ";
                }
                cout << "cost: " << costMetric[i][j] << endl;
            }
        }
    }
    exit(0);
}



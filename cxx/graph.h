#ifndef __graph_h__
#define __graph_h__

#include <string>
#include <vector>

struct Edge {
    std::string     fromNode;
    std::string     toNode;
    unsigned int    cost;

    Edge(std::string f, std::string t, unsigned int c=1)
        : fromNode(f), toNode(t), cost(c) {}
};
    
typedef std::vector<Edge> EdgeCollection;

bool loadGraph(const char* fileName, EdgeCollection& edges);

#endif


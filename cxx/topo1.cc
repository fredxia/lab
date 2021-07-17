//
// Topological sort by ingress degree
//
#include <assert.h>
#include <map>
#include <set>
#include <vector>
#include <utility>
#include <algorithm>
#include <iostream>
#include <list>
#include "graph.h"

using namespace std;

typedef pair<string, set<string> > IngressNode;

bool sortFunc(const IngressNode& a, const IngressNode& b)
{
    if (a.second.size() < b.second.size()) {
        return true;
    }
    if (a.second.size() == b.second.size()) {
        return a.first < b.first; // alphabetical order
    }
    return false;
}

int topoSort(const EdgeCollection& edges)
{
    // Create ingress mapping
    map<string, set<string> > ingressNodes;
    for (auto & edge : edges) {
        if (ingressNodes.find(edge.fromNode) == ingressNodes.end()) {
            ingressNodes[edge.fromNode] = set<string>();
        }
        ingressNodes[edge.toNode].insert(edge.fromNode);
    }

    // Convert mapping to vector and Sort by number of ingress degrees
    vector<IngressNode> sortedIngressNodes(ingressNodes.begin(),
                                           ingressNodes.end());
    sort(sortedIngressNodes.begin(), sortedIngressNodes.end(), sortFunc);

    // Copy vector to a list for efficient removal
    list<IngressNode> ingressNodeList(sortedIngressNodes.begin(),
                                      sortedIngressNodes.end());

    vector<string> result;

    // Pick from ingressNodeList those that has no incoming edges to seed
    // the initial result vector
    auto iter = ingressNodeList.begin();
    while (iter->second.size() == 0) {
        result.push_back(iter->first);
        iter = ingressNodeList.erase(iter);
    }

    // Start topo sorting. For each node in result walk ingressNodeList
    // and remove edge. If the node has zero ingress degree append it into
    // result set.
    unsigned int current  = 0;
    while (ingressNodeList.size() > 0) {
        auto currentNode = result[current];
        iter = ingressNodeList.begin();
        while (iter != ingressNodeList.end()) {
            auto found = iter->second.find(currentNode);
            if (found != iter->second.end()) {
                iter->second.erase(found);
                if (iter->second.size() == 0) {
                    result.push_back(iter->first);
                    iter = ingressNodeList.erase(iter);
                } else {
                    iter++;
                }
            } else {
                iter++;
            }
        }
        current++;
        // If result set is exhausted and there are still nodes in
        // ingressNodeList there must be a cycle.
        assert(current < result.size());
    }

    for (auto s : result) {
        cout << s << endl;
    }
    return 0;
}


void traverseTree(string node,
                  const map<string, set<string> >& treeNodes,
                  vector<string>& result)
{
    auto it = treeNodes.find(node);
    if (it != treeNodes.end()) {
        for (auto & n : it->second) {
            result.push_back(n);
        }
        for (auto & n : it->second) {        
            traverseTree(n, treeNodes, result);
        }
    }
}

int dfsVisit(string thisNode,
             const map<string, set<string> >& egressNodes,
             map<string, string>& parents,
             set<string>& topNodes)
{
    auto it = egressNodes.find(thisNode);
    if (it != egressNodes.end()) {
        for (auto & n : it->second) {
            if (parents.find(n) == parents.end()) {
                auto tt = topNodes.find(n);
                if (tt != topNodes.end()) {
                    topNodes.erase(tt);
                }
                parents[n] = thisNode;
                dfsVisit(n, egressNodes, parents, topNodes);
            }
        }
    }
    return 0;
}

int topoSortDfs(const EdgeCollection& edges)
{
    // Create egress mapping
    map<string, set<string> > egressNodes;
    for (auto & edge : edges) {
        egressNodes[edge.fromNode].insert(edge.toNode);
    }

    map<string, string> parents;

    set<string> topNodes;
    for (auto & n : egressNodes) {
        topNodes.insert(n.first);
    }

    for (auto & n : egressNodes) {
        dfsVisit(n.first, egressNodes, parents, topNodes);
    }

    // Add a root for top nodes
    string rootNode("ROOT");
    for (auto & n : topNodes) {
        cout << "top " << n << endl;
        parents[n] = rootNode;
    }

    // Construct the tree
    map<string, set<string> > treeNodes;
    for (auto & n : parents) {
        treeNodes[n.second].insert(n.first);
    }
    
    vector<string> result;
    traverseTree(rootNode, treeNodes, result);
    for (auto it = result.begin(); it != result.end(); it++) {
        cout << *it << ", ";
    }
    cout << endl;
    return 0;
}

int main(int argc, char** argv)
{
    EdgeCollection edges;
    if (!loadGraph(argv[1], edges)) {
        exit(1);
    }

    size_t sz = edges.size();
    assert(sz > 0);
    topoSort(edges);
    topoSortDfs(edges);
    exit(0);
}


#!/usr/bin/python3

import pdb
import copy
import sys
import traceback

def isInteractive(fh):
    return fh.isatty() and not fh.closed

def exceptionHook(ex, val, tr):
    traceback.print_exception(ex, val, tr)
    if isInteractive(sys.stderr) and isInteractive(sys.stdout):
        pdb.post_mortem(tr)

sys.excepthook = exceptionHook

all_nodes = {}

class Node:
    def __init__(self, name):
        self.name = name
        self.ingress_nodes = set([])
        self.egress_nodes = set([])

    def add_egress_node(self, node):
        assert node.name not in self.egress_nodes and \
            self.name not in node.ingress_nodes
        self.egress_nodes.add(node.name)
        node.ingress_nodes.add(self.name)

    def is_root(self):
        return not self.ingress_nodes

    def is_leaf(self):
        return not self.egress_nodes

def get_all_paths(root_node):
    assert root_node.is_root()

    # index of node => ingress nodes
    ingress_xrefs = {}
    leafs = set([])

    def traverse_node(node):
        if node.is_leaf():
            leafs.add(node.name)
            return

        for name in node.egress_nodes:
            if not name in ingress_xrefs:
                ingress_xrefs[name] = set([node.name])
            else:
                ingress_xrefs[name].add(node.name)
            traverse_node(all_nodes[name])

    traverse_node(root_node)
    print("ingress_xrefs %s, leafs %s" % (
        len(ingress_xrefs), len(leafs)))

    def build_paths(node, paths):
        assert not node.is_root()
        paths_copy = []
        while paths:
            paths_copy.append(paths.pop(0))
        for name in ingress_xrefs[node.name]:
            new_paths = copy.deepcopy(paths_copy)
            for p in new_paths:
                p.append(name)
            if not all_nodes[name].is_root():
                build_paths(all_nodes[name], new_paths)
            # TBD cache intermediate paths
            paths.extend(new_paths)

    all_paths = []
    for leaf in leafs:
        for name in ingress_xrefs[leaf]:
            paths = [ [leaf, name] ]
            node = all_nodes[name]
            if not node.is_root():
                build_paths(node, paths)
            all_paths.extend(paths)

    for p in all_paths:
        p.reverse()

    return { "/".join(p) for p in all_paths }


def get_all_paths_2(root_node):
    all_paths = []

    def dfs_walk(node, path):
        if not node.egress_nodes:
            all_paths.append(copy.deepcopy(path))
            return path
        for e in node.egress_nodes:
            path.append(e)
            dfs_walk(all_nodes[e], path)
            path.pop(-1)

    path = [root_node.name]
    dfs_walk(root_node, path)

    return [ "/".join(p) for p in all_paths ]
            
edges = [
    ( "1" , "2" ),
    ( "1" , "3" ),
    ( "1" , "10" ), 
    ( "2" , "4"),
    ( "2" , "3"),
    ( "10" , "7"),
    ( "10" , "8"),
    ( "3" , "5"),
    ( "3" , "7"),
    ( "3" , "4"),
    ( "4" , "6"),
    ( "5" , "6"),
    ( "5" , "9"),
    ( "8" , "9" ) ]

def main(nodes):
    for e in edges:
        if not e[0] in nodes:
            enode = Node(e[0])
            nodes[e[0]] = enode
        else:
            enode = nodes[e[0]]
        if not e[1] in nodes:
            inode = Node(e[1])
            nodes[e[1]] = inode
        else:
            inode = nodes[e[1]]
        enode.add_egress_node(inode)

    root = nodes["1"]
    result = get_all_paths(root)
    result2 = get_all_paths_2(root)
    assert len(result) == len(result2) and set(result) == set(result2)
    for p in result2:
        print(p)

main(all_nodes)


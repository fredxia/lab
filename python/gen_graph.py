#!/usr/bin/python3
#
# Generate a random DAG
#
import sys, random, click

def nodeName(level, levelCount):
    return "n%d_%d" % (level, random.randint(0, levelCount - 1))

@click.command()
@click.option("--maxBreadth", default=3, help="Max breadth")
@click.option("--maxDepth", default=3, help="Max depth")
@click.option("--maxEdges", default=10, help="Max number of edges")
@click.option("--maxCost", default=1, help="Max cost of an edge")
def genGraph(maxbreadth, maxdepth, maxedges, maxcost):
    levelNodeCount = {}
    edges = {}
    for level in range(maxdepth):
        levelNodeCount[level] = random.randint(1, maxbreadth)
    for _ in range(0, maxedges):
        fromLevel = random.randint(0, maxdepth - 2)
        toLevel = random.randint(fromLevel + 1, maxdepth - 1)
        cost = 1 if maxcost == 1 else random.randint(1, maxcost)
        fromNode = nodeName(fromLevel, levelNodeCount[fromLevel])
        toNode = nodeName(toLevel, levelNodeCount[toLevel])
        edges[(fromNode, toNode)] = cost
    for e in edges:
        if maxcost == 1:
            print("%s,%s" % (e[0], e[1]))
        else:
            print("%s,%s,%s" %(e[0], e[1], edges[e]))

if __name__=="__main__":
    genGraph()
    



    
    
    

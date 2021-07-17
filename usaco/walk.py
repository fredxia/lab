#!/usr/bin/python
#
# The problem: walk from left-bottom to the top-right of the grid.
# Can only move up or move right. Find the least cost path.
#
# The problem can be solved as:
#
# PathCost(x,y) = Min(PathCost(x-1, y) + Cost(x-1, y),
#                     PathCost(x, y-1) + Cost(x, y-1))
#
# Edge cases: along X and Y borders can only move right or move up.
#
import copy

# returns cost, steps
def walk(myarray, x, y):
    if x == 0 and y == 0:
        return myarray[x][y], [ (0, 0) ]
    if x == 0:
        # can only go up
        cost, steps = walk(myarray, 0, y - 1)
        steps.append( (0, y) )
        return cost + myarray[0][y], steps
    if y == 0:
        # can only go right
        cost, steps = walk(myarray, x - 1, 0)
        steps.append( (x, 0) )
        return cost + myarray[x][0], steps
        
    cost1, steps1 = walk(myarray, x - 1, y)
    cost2, steps2 = walk(myarray, x, y - 1)
    
    if cost1 > cost2:
        steps1.append( (x, y) )
        return cost1 + myarray[x][y], steps1
    else:
        steps2.append( (x, y) )
        return cost2 + myarray[x][y], steps2

myarray1 = [ [ 5, 2, 3, 4, 5 ],
             [ 5, 2, 3, 4, 5 ],
             [ 5, 5, 5, 5, 5 ],
             [ 1, 2, 3, 4, 5 ],
             [ 1, 2, 3, 4, 5 ] ]

cost, steps = walk(myarray1, 4, 4)
print cost
print steps

myarray2 = [ [ 9, 9, 9, 9, 9, 9, 9, 9, 9 ],
             [ 1, 8, 7, 6, 5, 9, 3, 2, 9 ],
             [ 1, 2, 9, 4, 5, 9, 7, 8, 9 ],
             [ 2, 9, 9, 8, 9, 9, 3, 2, 9 ],
             [ 3, 2, 3, 4, 9, 6, 7, 8, 9 ],
             [ 4, 8, 7, 6, 5, 8, 3, 2, 9 ],
             [ 5, 2, 3, 4, 5, 6, 9, 8, 9 ],
             [ 6, 8, 7, 6, 5, 4, 3, 8, 9 ],
             [ 9, 2, 3, 4, 5, 6, 7, 8, 9 ] ]

cost, steps = walk(myarray2, 8, 8)
print cost, len(steps)
print steps

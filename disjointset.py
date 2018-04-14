from collections import defaultdict
from functools import namedtuple

class DisjointSet(object):
    """
    A DisjointSet tracks a set of objects partitioned into disjoint subsets.
    """

    def __init__(self):
        self.nodes = {}

    def find(self, x):
        """
        Finds a representative element of the partition that `x` belongs to. 
        """
        # if x is not in the set, add it.
        if x not in self.nodes:
            self.nodes[x] = Node(x, 1)
            return x
        # otherwise, find the root.
        x = self.nodes[x]
        while x != x.parent:
            x.parent = x.parent.parent # perform path halving
            x = x.parent
        return x.value

    def merge(self, x, y):
        """
        Unifies the partitions that `x` and `y` belong to.

        The representative of the partition `x` belongs to is the
        representative of the new partition.
        """
        # find the roots of x and y.
        xroot = self.nodes[self.find(x)]
        yroot = self.nodes[self.find(y)]
        # x and y are already unified, we are done.
        if xroot == yroot: return
        # ensure that xroot.size >= yroot.size
        if xroot.size < yroot.size:
            xroot, yroot = yroot, xroot
            # ensure that the respresentative of parition `x` is the 
            # representative of the new partition
            xroot.value, yroot.value = yroot.value, xroot.value
            self.nodes[xroot.value] = xroot
            self.nodes[yroot.value] = yroot
        # make xroot the parent of yroot
        yroot.parent = xroot
        xroot.size += yroot.size

class Node(object):
    def __init__(self, value):
        self.parent = self
        self.value = value
        self.size = 1

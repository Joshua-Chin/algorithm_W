from collections import defaultdict
from functools import namedtuple

from data import type_variable

__all__ = ['UnionFind']

class UnionFind(object):
    """
    A UnionFind data structure tracks a set of objects partitioned into
    disjoint subsets.

    In particular, this data structure is used to track type unifications.
    """

    def __init__(self):
        self._nodes = {}

    def find(self, x):
        """
        Finds a representative element of the partition that `x` belongs to. 
        """
        # x is disjoint
        if x not in self._nodes:
            self._nodes[x] = node(x, 1)
            return x
        # x is contained in the grap
        return self._find_root(self._nodes[x]).value

    def _find_root(self, node):
        if node == node.parent:
            return node
        root = self._find_root(node.parent)
        node.parent = root
        return root

    def unify(self, x, y):
        """
        Unifies the partition that x belongs to and the partition that y belongs to.
        """
        # find the roots of x and y
        x = self._find_root(self._nodes[x])
        y = self._find_root(self._nodes[y])
        # x and y are already unified
        if x == y:
            return
        # ensure the x has greater size
        if x.size < y.size:
            x, y = y, x
        # swap the values of x and y if x is a type variable
        if isinstance(x.value, type_variable):
            x.value, y.value = y.value, x.value
        # make x the parent of y
        y.parent = x
        x.size += y.size

    def __contains__(self, x):
        return x in self._nodes

    def __iter__(self):
        yield from self._nodes

    def __len__(self):
        return len(self._nodes)

    def __repr__(self):
        partitions = defaultdict(list)
        for elem in self._nodes:
            partitions[self.find(elem)].append(elem)
        return repr(dict(partitions))

class node(object):

    def __init__(self, value, size, parent=None):
        self.value = value
        self.size = size
        self.parent = parent if parent is not None else self

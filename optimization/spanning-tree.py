#!/usr/bin/env python
# -+- coding: utf-8 -*-

"""minimal spanning tree.py

A python script that applies the well-known Kruskal's algorithm to a graph in
order to output a minimal cost to connect each city in a graph. The algorithm
takes into consideration that the cost is how much is spent to connect two
cities.
"""

from __future__ import absolute_import, division

from collections import defaultdict
from heapq import heappop, heappush
from random import random, randrange, seed
from typing import List, Set, Tuple

class Graph:
    """
    Graph class to improve algorithm implementation

    :param v: List of vertexes
    :param e: List of edges
    """
    vertex = Set[int]
    v_size = 0
    edges = Set[Tuple[int, int, float]]
    e_size = 0

    def __init__(self, v, e):
        self.vertex = v
        self.edges = e
        self.v_size = len(v)
        self.e_size = len(e)


def kruskal(graph: Graph) -> Set[Tuple[int, int, float]]:
    """
    Kruskal's algorithm from CLRS (Introduction to Algorithms, Section 23.2),
    using the Timsort algorithm.

    :param graph: Graph structure used to find the minimal spanning tree.
    :return: List of edges that form the minimum spanning tree.
    """
    A = set()
    S = [{x} for x in range(graph.v_size)]
    edges_sorted = sorted(graph.edges, key=lambda tup: tup[2]) # n log n
    for e in edges_sorted:
        if S[e[0]] != S[e[1]]:
            A.add(e)

            U = S[e[0]].union(S[e[1]])
            for w in U:
                S[w] = U
    return A

def mst_triple_degree(graph: Graph) -> Set[Tuple[int, int, float]]:
    """
    Wrapper function that applies the minimal spanning tree algorithm on a graph
    G and sweeps the edge list to locate the vertex with degree 3 or more. The
    sweep is done with each vertex from the edges (undirected graph).

    :param graph: Graph structure used to find de minimal spanning tree.
    :return: The vertexes with 3 or more edges.
    """
    k_edges = kruskal(graph)
    count_list = defaultdict(int)

    for e in k_edges:
        count_list[e[0]] += 1
        count_list[e[1]] += 1

    return {e for e, c in count_list.items() if c >= 3}

if __name__ == "__main__":
    g = Graph(
        {0,1,2,3,4,5,6},
        {
            (0,1,10), (1,2,15), (1,6,200), (1,3,200),
            (2,3,20), (2,4,10), (2,5,10)
        })
    print(mst_triple_degree(g))

#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""spanning_tree.py

A python script that applies the well-known Kruskal's algorithm to a graph in
order to output a minimal cost to connect each city in a graph. The algorithm
takes into consideration that the cost is how much is spent to connect two
cities.
"""

from collections import defaultdict
from random import randint, seed
from typing import Set, Tuple


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

    def kruskal(self) -> Set[Tuple[int, int, float]]:
        """
        Kruskal's algorithm from CLRS (Introduction to Algorithms, Section 23.2),
        using the Timsort algorithm.

        :param graph: Graph structure used to find the minimal spanning tree.
        :return: List of edges that form the minimum spanning tree.
        """
        minimal_edges_set = set()
        vertex_sets = [{x} for x in range(self.v_size)]
        edges_sorted = sorted(self.edges, key=lambda tup: tup[2])
        for edge in edges_sorted:
            if vertex_sets[edge[0]] != vertex_sets[edge[1]]:
                minimal_edges_set.add(edge)

                tmp_vertex_set = vertex_sets[edge[0]].union(vertex_sets[edge[1]])
                for vertex in tmp_vertex_set:
                    vertex_sets[vertex] = tmp_vertex_set
        return minimal_edges_set

    def mst_triple_degree(self) -> Set[Tuple[int, int, float]]:
        """
        Wrapper function that applies the minimal spanning tree algorithm on a graph
        G and sweeps the edge list to locate the vertex with degree 3 or more. The
        sweep is done with each vertex from the edges (undirected graph).

        :param graph: Graph structure used to find de minimal spanning tree.
        :return: The vertexes with 3 or more edges.
        """
        k_edges = self.kruskal()
        count_list = defaultdict(int)

        for edge in k_edges:
            count_list[edge[0]] += 1
            count_list[edge[1]] += 1

        return {edge for edge, count in count_list.items() if count >= 3}


def random_tests(order: int, connections: int, limit: int = 128, tests: int = 1000):
    """
    Creates random sets of parameters to test the algorithms above.

    :param order:         Integer representing the number of vertexes.
    :param connections:   Integer representing the number of edges.
    :param limit:         Integer representing the maximum value for all edges and
                          other parameters.
    :param tests:         Integer representing the number of tests to run.
    """
    seed(1)

    for iteration in range(tests):
        vertexes = {vertex for vertex in range(order)}
        edges = {
            (randint(0, order - 1), randint(0, order - 1), randint(0, limit))
            for _ in range(connections)
        }

        print("------ Test ", iteration, " ------")
        print("Vertexes with 3-degree or more: ")
        print(Graph(vertexes, edges).mst_triple_degree())
        print("-------------------")


if __name__ == "__main__":
    random_tests(128, 128)

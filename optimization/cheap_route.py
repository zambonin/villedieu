#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0330, R0913

"""cheap_route.py

A Python script that applies the well-known Dijkstra's algorithm to a graph
in order to output the cheapest route between two cities, taking into account
toll roads and a static vehicle autonomy.
"""

from __future__ import absolute_import, division

from heapq import heappop, heappush
from random import random, randrange, seed
from typing import List, Tuple


def dijkstra(
    graph: List[List[float]], source: int
) -> Tuple[List[float], List[int]]:
    """
    Dijkstra's algorithm from CLRS (Introduction to Algorithms, Section 24.3),
    slightly modified to start with a different min-priority queue and
    actually return data.

    :param graph:   Adjacency matrix with values in the currency unit.
    :param source:  Integer representing the source vertex.
    :return:        Distances between the source and all vertices in the
                    graph, and a list of hops that represent the shortest path.
    """
    dist = [float("inf")] * len(graph)  # initialize-single-source
    dist[source] = 0
    prev = [-1] * len(graph)

    vertices = []
    heappush(vertices, (dist[source], source))
    neighbors = [
        (index for index, edge in enumerate(row) if edge) for row in graph
    ]

    while vertices:
        _, curr = heappop(vertices)
        for vert in neighbors[curr]:
            alt = dist[curr] + graph[curr][vert]
            if dist[vert] > alt:  # relaxation
                dist[vert] = alt
                prev[vert] = curr
                heappush(vertices, (alt, vert))

    return dist, prev


def cheapest_route(
    graph: List[List[int]],
    tolls: List[float],
    source: int,
    dest: int,
    gas_price: float,
    autonomy: float,
) -> Tuple[List[int], float]:
    """
    Wrapper function that takes into account the parameters and transforms
    the graph accordingly, converting from kilometers to currency and adding
    the toll prices to all successors of a vertex. Furthermore, it constructs
    the shortest path by reverse iteration of the hops given by Dijkstra's
    algorithm.

    :param graph:       Adjacency matrix representing a directed and weighted
                        graph, with units in kilometers. The set of vertices
                        is simply the non-negative integer numbers.
    :param tolls:       Function between the set of vertices and the positive
                        real numbers, represented as the mapping itself.
    :param source:      Integer representing the source vertex.
    :param dest:        Integer representing the destination vertex.
    :param gas_price:   A real value representing the gas price.
    :param autonomy:    A real value representing the kilometer per liter ratio.
    :return:            The shortest path between `source` and `dest`,
                        and its cost.
    """
    assert len(graph) != 0
    assert len(graph) == len(graph[0]) == len(tolls)
    assert source <= len(graph) and dest <= len(graph)

    mod_graph = [
        [(edge * gas_price / autonomy) + toll if edge else 0 for edge in row]
        for row, toll in zip(graph, tolls)
    ]

    dist, prev = dijkstra(mod_graph, source)
    path, curr = [], dest

    while prev[curr] >= 0:
        path.append(curr)
        curr = prev[curr]
    path.append(curr)
    path.reverse()

    return path, dist[dest]


def random_tests(order: int, limit: int = 128, tests: int = 1000):
    """
    Creates random sets of parameters to test the algorithms above.

    :param order:   Integer representing the side of the adjacency matrix.
    :param limit:   Integer representing the maximum value for all edges and
                    other parameters.
    :param tests:   Integer representing the number of tests to run.
    """
    seed(1)
    for _ in range(tests):
        graph = [
            [limit * random() if i != j else 0 for i in range(order)]
            for j in range(order)
        ]
        tolls = [limit * random() for _ in range(order)]
        source, dest = randrange(order), randrange(order)
        while source == dest:
            dest = randrange(order)
        gas_price, autonomy = limit * random(), limit * random()

        print(cheapest_route(graph, tolls, source, dest, gas_price, autonomy))


def known_tests():
    """
    Creates known graphs and tests the results from the implemented algorithms.
    """
    # Regular graph with pure dijkstra.
    graph = [
        [0,4,0,0,0,0,0,8,0],
        [4,0,8,0,0,0,0,11,0],
        [0,8,0,7,0,4,0,0,2],
        [0,0,7,0,9,14,0,0,0],
        [0,0,0,9,0,10,0,0,0],
        [0,0,4,14,10,0,2,0,0],
        [0,0,0,0,0,2,0,1,6],
        [8,11,0,0,0,0,1,0,7],
        [0,0,2,0,0,0,6,7,0]
    ]
    tolls = [0,0,0,0,0,0,0,0,0]

    assert cheapest_route(graph, tolls, 0, 4, 1, 1) == ([0,7,6,5,4], 21)

    # Regular graph with known result and no tolls.
    graph = [
        [0,10,5,0],
        [10,0,0,20],
        [5,0,0,30],
        [0,20,30,0]
    ]
    tolls = [0,0,0,0]

    assert cheapest_route(graph, tolls, 0, 3, 5, 2) == ([0,1,3], 75)

    # Regular graph with known result and tolls.
    graph = [
        [0,10,5,0],
        [10,0,0,20],
        [5,0,0,30],
        [0,20,30,0]
    ]
    tolls = [10,20,5,5]

    assert cheapest_route(graph, tolls, 0, 3, 5, 2) == ([0,2,3], 102.5)

    # Graph with no edges.
    graph = [
        [],
        [],
        [],
        []
    ]

    tolls = [10,20,5,5]

    try:
        cheapest_route(graph, tolls, 0, 3, 5, 2)
    except AssertionError:
        print("The parameters were not defined as expected!")

    # Graph with no vertexes and edges.
    graph = []

    tolls = [10,20,5,5]

    try:
        cheapest_route(graph, tolls, 0, 3, 5, 2)
    except AssertionError:
        print("The parameters were not defined as expected!")

    # Graph with no tolls.
    graph = [
        [0,10,5,0],
        [10,0,0,20],
        [5,0,0,30],
        [0,20,30,0]
    ]

    tolls = []

    try:
        cheapest_route(graph, tolls, 0, 3, 5, 2)
    except AssertionError:
        print("The parameters were not defined as expected!")

    # Graph with invalid source.
    graph = [
        [0,10,5,0],
        [10,0,0,20],
        [5,0,0,30],
        [0,20,30,0]
    ]

    tolls = []

    try:
        cheapest_route(graph, tolls, 0, 3, 100, 2)
    except AssertionError:
        print("The parameters were not defined as expected!")

    # Graph with invalid destination.
    graph = [
        [0,10,5,0],
        [10,0,0,20],
        [5,0,0,30],
        [0,20,30,0]
    ]

    tolls = []

    try:
        cheapest_route(graph, tolls, 0, 3, 5, 100)
    except AssertionError:
        print("The parameters were not defined as expected!")

if __name__ == "__main__":
    # random_tests(128)
    known_tests()

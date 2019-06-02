#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0330, R0913

from __future__ import absolute_import, division

from heapq import heappop, heappush
from random import random, randrange, seed
from typing import List, Tuple


def dijkstra(
    graph: List[List[float]], source: int
) -> Tuple[List[float], List[int]]:

    dist = [float("inf")] * len(graph)
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
            if alt < dist[vert]:
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


def known_answer():
    # http://web.stanford.edu/class/archive/cs/cs106b/cs106b.1152/images/graph-dijkstra-figure-1.png
    graph = [
        [0, 4, 0, 2, 7, 0, 0, 0],
        [0, 0, 0, 0, 2, 0, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 4],
        [0, 0, 0, 0, 0, 2, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 2],
        [0, 0, 0, 0, 5, 1, 0, 0],
    ]

    tolls = [1, 2, 3, 4, 5, 6, 7, 8]
    source = 0
    dest = 5
    gas_price = 2
    autonomy = 5

    assert cheapest_route(graph, tolls, source, dest, gas_price, autonomy) == (
        [0, 4, 5],
        9.6,
    )


if __name__ == "__main__":
    known_answer()
    random_tests(128)

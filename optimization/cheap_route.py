#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List, Tuple


def dijkstra(graph: List[List[float]], source: int) -> Tuple[List[int]]:

    dist = [float("inf")] * len(graph)
    dist[source] = 0

    prev = [None] * len(graph)
    vertices = set(range(len(graph)))

    while vertices:
        curr = min(vertices, key=lambda v: dist[v])
        vertices.remove(curr)

        for v in set(graph[curr].index(e) for e in graph[curr] if e):
            alt = dist[curr] + graph[curr][v]
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = curr

    return dist, prev


def q1(
    graph: List[List[int]],
    tolls: List[float],
    source: int,
    dest: int,
    gas_price: float,
    autonomy: float,
) -> List[int]:

    assert len(graph) == len(graph[0]) == len(tolls)
    assert source <= len(graph) and dest <= len(graph)

    mod_graph = [
        list(map(lambda x: (x * gas_price / autonomy) + toll if x else 0, row))
        for row, toll in zip(graph, tolls)
    ]

    dist, prev = dijkstra(mod_graph, source)
    path, curr = [], dest

    while prev[curr] is not None:
        path.append(curr)
        curr = prev[curr]
    path.append(curr)
    path.reverse()

    return path, dist[dest]


if __name__ == "__main__":
    # http://web.stanford.edu/class/archive/cs/cs106b/cs106b.1152/images/graph-dijkstra-figure-1.png
    g = [
        [0, 4, 0, 2, 7, 0, 0, 0],
        [0, 0, 0, 0, 2, 0, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 4],
        [0, 0, 0, 0, 0, 2, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 2],
        [0, 0, 0, 0, 5, 1, 0, 0],
    ]

    p = [1, 2, 3, 4, 5, 6, 7, 8]
    s = 0
    d = 5
    gp = 2
    a = 5

    print(q1(g, p, s, d, gp, a))

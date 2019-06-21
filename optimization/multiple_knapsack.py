#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0330

"""multiple_knapsack.py

A Python script to approximate good solutions for the multiple 0-1 knapsack
problem, using both dynamic programming and greedy approaches, respectively
with one and multiple knapsacks.
"""

from __future__ import absolute_import, division

from collections import defaultdict, namedtuple
from functools import lru_cache
from typing import Dict, List, Set, Tuple
from sys import maxsize

Item = namedtuple("Item", ["value", "weight"])


def knapsack(items: List[Item], max_weight: int) -> Tuple[int, List[Item]]:
    """Solve the knapsack problem by finding the most valuable subsequence
    of items that weighs no more than a certain threshold. Based on [1].

    [1] https://codereview.stackexchange.com/a/20581

    :param items:       Pairs of non-negative integers in the form (value,
                        weight).
    :param max_weight:  Capacity of the knapsack as a non-negative integer.
    :return:            The sum of values in the most valuable subsequence, and
                        the subsequence itself.

    >>> items = [Item(4, 12), Item(2, 1), Item(6, 4), Item(1, 1), Item(2, 2)]
    >>> knapsack(items, 15)
    (11,
     [Item(value=2, weight=1),
      Item(value=6, weight=4),
      Item(value=1, weight=1),
      Item(value=2, weight=2)])
    """

    @lru_cache(maxsize=None)
    def best_value(i: int, j: int) -> int:
        """
        Return the value of the most valuable subsequence of the first
        `i` elements in `items` whose weights sum no more than `j`.
        """
        if j < 0:
            return -maxsize - 1
        if i == 0:
            return 0
        value, weight = items[i - 1]
        return max(best_value(i - 1, j), best_value(i - 1, j - weight) + value)

    n_items = len(items)
    tmp_max = max_weight
    result = []

    for index in range(n_items - 1, 0, -1):
        if best_value(index + 1, tmp_max) != best_value(index, tmp_max):
            result.append(items[index])
            tmp_max -= items[index].weight

    return best_value(n_items, max_weight), list(reversed(result))


def mkp(items: List[Item], trucks: List[int]) -> Dict[int, Set[Item]]:
    """
    Rough solutions to the multiple 0-1 knapsack problem using a greedy
    approach, i.e. the hardest knapsack to fill goes first.

    :param trucks:  Integers that represent the capacity of each knapsack.
    :param items:   Pairs of non-negative integers in the form (value, weight).
    :return:        The listing of items inside each knapsack, or truck.

    >>> trucks = [5, 7, 8]
    >>> items = [Item(5, 3), Item(10, 8), Item(8, 7), Item(7, 5)]
    >>> mkp(items, trucks)
    {5: {Item(value=7, weight=5)},
     7: {Item(value=8, weight=7)},
     8: {Item(value=10, weight=8)}}
    """
    solution = defaultdict(set)

    for capacity in sorted(trucks):
        _, result = knapsack(items, capacity)
        if result:
            solution[capacity] = set(result)
        for used_item in result:
            items.remove(used_item)

    return dict(solution)


def known_tests_single():
    """
    Simple 0-1 knapsack tests from [1].

    [1] https://people.sc.fsu.edu/~jburkardt/datasets/knapsack_01/
    """
    trucks = [165, 26, 190, 50, 104, 170, 750, 6404180]
    items = [
        [
            Item(value, weight)
            for value, weight in zip(
                [92, 57, 49, 68, 60, 43, 67, 84, 87, 72],
                [23, 31, 29, 44, 53, 38, 63, 85, 89, 82],
            )
        ],
        [
            Item(value, weight)
            for value, weight in zip([24, 13, 23, 15, 16], [12, 7, 11, 8, 9])
        ],
        [
            Item(value, weight)
            for value, weight in zip(
                [50, 50, 64, 46, 50, 5], [56, 59, 80, 64, 75, 17]
            )
        ],
        [
            Item(value, weight)
            for value, weight in zip(
                [70, 20, 39, 37, 7, 5, 10], [31, 10, 20, 19, 4, 3, 6]
            )
        ],
        [
            Item(value, weight)
            for value, weight in zip(
                [350, 400, 450, 20, 70, 8, 5, 5], [25, 35, 45, 5, 25, 3, 2, 2]
            )
        ],
        [
            Item(value, weight)
            for value, weight in zip(
                [442, 525, 511, 593, 546, 564, 617],
                [41, 50, 49, 59, 55, 57, 60],
            )
        ],
        [
            Item(value, weight)
            for value, weight in zip(
                [
                    135,
                    139,
                    149,
                    150,
                    156,
                    163,
                    173,
                    184,
                    192,
                    201,
                    210,
                    214,
                    221,
                    229,
                    240,
                ],
                [
                    70,
                    73,
                    77,
                    80,
                    82,
                    87,
                    90,
                    94,
                    98,
                    106,
                    110,
                    113,
                    115,
                    118,
                    120,
                ],
            )
        ],
        [
            Item(value, weight)
            for value, weight in zip(
                [
                    825594,
                    1677009,
                    1676628,
                    1523970,
                    943972,
                    97426,
                    69666,
                    1296457,
                    1679693,
                    1902996,
                    1844992,
                    1049289,
                    1252836,
                    1319836,
                    953277,
                    2067538,
                    675367,
                    853655,
                    1826027,
                    65731,
                    901489,
                    577243,
                    466257,
                    369261,
                ],
                [
                    382745,
                    799601,
                    909247,
                    729069,
                    467902,
                    44328,
                    34610,
                    698150,
                    823460,
                    903959,
                    853665,
                    551830,
                    610856,
                    670702,
                    488960,
                    951111,
                    323046,
                    446298,
                    931161,
                    31385,
                    496951,
                    264724,
                    224916,
                    169684,
                ],
            )
        ],
    ]
    optimal = [
        "1111010000",
        "01110",
        "110010",
        "1001000",
        "10111011",
        "0101001",
        "101010111000011",
        "110111000110100100000111",
    ]

    for truck, item, opt in zip(trucks, items, optimal):
        profit = sum(
            item.value for item, present in zip(item, opt) if int(present)
        )
        solution = mkp(item, [truck])
        sol_values = sum(
            sum(item.value for item in _set) for _set in solution.values()
        )
        print("{:>7.2%} of optimal profit".format(sol_values / profit))


def known_tests_multiple():
    """
    Multiple 0-1 knapsack tests from [1].

    [1] https://people.sc.fsu.edu/~jburkardt/datasets/knapsack_multiple/
    """
    trucks = [
        [70, 127],
        [50, 81, 120],
        [31, 37, 48, 152],
        [165],
        [65, 85],
        [103, 156],
    ]
    items = [
        [
            Item(value, weight)
            for value, weight in zip(
                [92, 57, 49, 68, 60, 43, 67, 84, 87, 72],
                [23, 31, 29, 44, 53, 38, 63, 85, 89, 82],
            )
        ],
        [
            Item(value, weight)
            for value, weight in zip(
                [92, 57, 49, 68, 60, 43, 67, 84, 87, 72],
                [23, 31, 29, 44, 53, 38, 63, 85, 89, 82],
            )
        ],
        [
            Item(value, weight)
            for value, weight in zip(
                [92, 57, 49, 68, 60, 43, 67, 84, 87, 72],
                [23, 31, 29, 44, 53, 38, 63, 85, 89, 82],
            )
        ],
        [
            Item(value, weight)
            for value, weight in zip(
                [92, 57, 49, 68, 60, 43, 67, 84, 87, 72],
                [23, 31, 29, 44, 53, 38, 63, 85, 89, 82],
            )
        ],
        [
            Item(value, weight)
            for value, weight in zip(
                [110, 150, 70, 80, 30, 5], [40, 60, 30, 40, 20, 5]
            )
        ],
        [
            Item(value, weight)
            for value, weight in zip(
                [78, 35, 89, 36, 94, 75, 74, 79, 80, 16],
                [18, 9, 23, 20, 59, 61, 70, 75, 76, 30],
            )
        ],
    ]
    optimal = [
        ["1001000000", "0110001000"],
        ["1000000000", "0101000000", "0010110000"],
        ["1000000000", "0100000000", "0001000000", "0010101000"],
        ["1111010000"],
        ["010001", "100100"],
        ["1010010000", "0001100010"],
    ]

    for truck, item, opt in zip(trucks, items, optimal):
        profit = sum(
            sum(i.value for i, j in zip(item, o) if int(j)) for o in opt
        )
        solution = mkp(item, truck)
        sol_values = sum(
            sum(item.value for item in _set) for _set in solution.values()
        )
        print("{:>7.2%} of optimal profit".format(sol_values / profit))


if __name__ == "__main__":
    known_tests_single()
    known_tests_multiple()

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

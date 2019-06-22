#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0111,C0330

"""activity_selection.py

A recursive implementation of the activity-selection problem, as per CLRS
(Introduction to Algorithms, Section 16.1), in its greedy polynomial version,
giving the optimal scheduling.
"""

from __future__ import absolute_import

from collections import namedtuple
from operator import itemgetter
from pprint import pprint
from random import randint
from typing import Set

Interval = namedtuple("Interval", ["start", "end"])


def gen_rand_intervals(
    _min: int = 1, _max: int = 100, _len: int = 100
) -> Set[Interval]:
    intervals = set()
    for _ in range(_len):
        start, end = 0, 0
        while start >= end:
            start, end = randint(_min, _max), randint(_min, _max)
        intervals.add(Interval(start=start, end=end))
    return intervals


def schedule(intervals: Set[Interval]) -> Set[Interval]:
    ans = set()
    if intervals:
        _min = min(intervals, key=itemgetter(1))
        ans.add(_min)
        removed = set(filter(lambda intv: intv.start > _min.end, intervals))
        ans.update(schedule(removed))
    return ans


if __name__ == "__main__":
    pprint(sorted(schedule(gen_rand_intervals())))

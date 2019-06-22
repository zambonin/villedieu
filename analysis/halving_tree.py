#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=C0111,W0603

"""halving_tree.py

Three separate implementations that print the number of nodes below the root
for a tree that, starts with `n` children and halves this number at each level.
For instance, if `n` is 3, one has twelve nodes, numbered below as if covered
by a breadth-first search.
                                      ┯
                    ┌───────────┬─────┴─────┬───────────┐
                    01         02           03         04
                ┌───┴───┐   ┌───┴───┐   ┌───┴───┐   ┌───┴───┐
                05     06   07     08   09     10   11     12
"""

from __future__ import absolute_import, division

from math import log2


def orig_rec(num: int) -> int:
    global COUNTER
    if num > 1:
        for _ in range(num):
            COUNTER += 1
            orig_rec(num // 2)
    return COUNTER


def simpl_rec(num: int) -> int:
    if num == 1:
        return 0
    return num * simpl_rec(num // 2) + num


def iter_form(num: int) -> int:
    return int(
        sum(
            (num ** i) / (2 ** (1 / 2 * i * (i - 1)))
            for i in range(1, int(log2(num) + 1))
        )
    )


if __name__ == "__main__":
    for k in range(3):
        COUNTER = 0
        assert orig_rec(1 << k) == simpl_rec(1 << k) == iter_form(1 << k)

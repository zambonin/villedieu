from collections import defaultdict
from functools import lru_cache


# https://codereview.stackexchange.com/a/20581
def knapsack(items, maxweight):
    """Solve the knapsack problem by finding the most valuable subsequence
    of items that weighs no more than maxweight.

    items must be a sequence of pairs (value, weight), where value is a
    number and weight is a non-negative integer.

    maxweight is a non-negative integer.

    Return a pair whose first element is the sum of values in the most
    valuable subsequence, and whose second element is the subsequence.

    >>> items = [(4, 12), (2, 1), (6, 4), (1, 1), (2, 2)]
    >>> knapsack(items, 15)
    (11, [(2, 1), (6, 4), (1, 1), (2, 2)])

    """
    @lru_cache(maxsize=None)
    def bestvalue(i, j):
        # Return the value of the most valuable subsequence of the first
        # i elements in items whose weights sum to no more than j.
        if j < 0:
            return float('-inf')
        if i == 0:
            return 0
        value, weight = items[i - 1]
        return max(bestvalue(i - 1, j), bestvalue(i - 1, j - weight) + value)

    j = maxweight
    result = []
    for i in reversed(range(len(items))):
        if bestvalue(i + 1, j) != bestvalue(i, j):
            result.append(items[i])
            j -= items[i][1]
    result.reverse()
    return bestvalue(len(items), maxweight), result


def greedy(trucks, items):
    solution = defaultdict(set)

    for capacity in sorted(trucks):
        _, result = knapsack(list(items), capacity)
        if result:
            solution[capacity] = set(result)
        for used_item in result:
            items.remove(used_item)

    return dict(solution)


if __name__ == "__main__":
    trucks = {5, 7, 8}
    # (value, weight)
    items = [(5, 3), (10, 8), (8, 7), (7, 5)]

    print(greedy(trucks, items))

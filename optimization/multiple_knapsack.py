from collections import defaultdict


def greedy(trucks, items):
    # sort trucks by capacity
    sorted_trucks = sorted(
        trucks.items(), key=lambda item: item[1], reverse=True)

    # sort items by value/weight ratio
    sorted_items = sorted(
        items.items(), key=lambda item: item[1][1]/item[1][0], reverse=True)

    solution = defaultdict(set)

    for truck, capacity in sorted_trucks:
        used_items = set()
        for item, (weight, value) in sorted_items:
            if weight <= capacity:
                used_items.add((item, (weight, value)))
                capacity -= weight
                solution[truck].add(item)
        for used_item in used_items:
            sorted_items.remove(used_item)

    return dict(solution)


if __name__ == "__main__":
    trucks = dict(enumerate({15,10,20}))
    items = dict(enumerate({
        # (weight, value)
        (3,5),
        (8,10),
        (7,8),
        (5,7),
    }))

    print(greedy(trucks, items))

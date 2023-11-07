import itertools
import math

def euclidean_distance(city1, city2):
    x1, y1 = city1
    x2, y2 = city2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def tsp_held_karp(cities):
    n = len(cities)
    all_points_set = set(range(n))

    # Create a memoization table to store subproblem solutions
    memo = {}
    
    # Initialize memoization table
    for k in range(1, n):
        memo[(1 << k, k)] = (euclidean_distance(cities[0], cities[k]), 0)
    
    for subset_size in range(2, n):
        for subset in itertools.combinations(range(n), subset_size):
            subset_mask = 0
            for city in subset:
                subset_mask |= 1 << city
            for k in subset:
                if k == 0:
                    continue
                prev_subset_mask = subset_mask ^ (1 << k)
                min_distance = float('inf')
                prev_city = -1
                for m in subset:
                    if m == 0 or m == k:
                        continue
                    distance = memo[(prev_subset_mask, m)][0] + euclidean_distance(cities[m], cities[k])
                    if distance < min_distance:
                        min_distance = distance
                        prev_city = m
                memo[(subset_mask, k)] = (min_distance, prev_city)
    
    # Reconstruct the shortest path
    subset_mask = (1 << n) - 1
    k = min(range(n), key=lambda k: memo[(subset_mask, k)][0])
    tour = [0]
    while k != 0:
        tour.append(k)
        subset_mask ^= 1 << k
        k = memo[(subset_mask, k)][1]
    
    tour.append(0)
    return [cities[i] for i in tour]

staedte_positionen = (
    (0.010319427306382911, 0.8956251389386756),
    (0.6999898714299346, 0.42254500074835377),
    (0.4294574582950912, 0.4568408794115657),
    (0.6005454852683483, 0.9295407203370832),
    (0.9590226056623925, 0.581453646599427),
    (0.748521134122647, 0.5437775417153159),
    (0.7571232013282426, 0.606435031856663),
    (0.07528757443413125, 0.07854082131763074),
    (0.32346175150639334, 0.7291706487873425)
)

shortest_path_in_order = tsp_held_karp(staedte_positionen)

print("Kuerzester Weg:", shortest_path_in_order)

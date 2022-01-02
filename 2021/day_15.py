from typing import Tuple
import functools
from collections import deque, defaultdict
import numpy as np
import networkx as nx

with open("i") as f:
    arr = np.array([list(map(int, line)) for line in f.read().splitlines()], dtype=int)


def get_neighbours(index: Tuple[int, int]):
    """Get the set of neighbouring indices of the given index, excluding indices outside the bounds of the array.

    Example input: (4, 5)
    Example output: {(4, 6), (4, 4), (3, 5), (5, 5)}"""
    s = [
        (index[0], index[1] - 1),
        (index[0], index[1] + 1),
        (index[0] - 1, index[1]),
        (index[0] + 1, index[1]),
    ]
    return [
        s[i]
        for i in range(4)
        if 0 <= s[i][0] < arr.shape[0] and 0 <= s[i][1] < arr.shape[1]
    ]


arr = np.tile(arr, (5, 5)) + np.repeat(
    np.repeat(np.arange(5)[:, None] + np.arange(5), len(arr), axis=0), len(arr), axis=1
)
arr %= 9
arr[arr == 0] = 9
print(
    str(arr)
    .replace("[", "")
    .replace("]", "")
    .replace(" ", "")
    .replace("0", "\033[1m0\033[0m")
)
print()

G = nx.DiGraph()
for index, weight in np.ndenumerate(arr):
    G.add_node(index)
    for neighbour in get_neighbours(index):
        G.add_node(neighbour)
        G.add_edge(index, neighbour, weight=arr[neighbour])

res = nx.shortest_path(
    G, (0, 0), (arr.shape[0] - 1, arr.shape[1] - 1), "weight", "bellman-ford"
)
r = sum(arr[i] for i in res[1:])

arr[tuple(zip(*res))] = 0
print(
    str(arr)
    .replace("[", "")
    .replace("]", "")
    .replace(" ", "")
    .replace("0", "\033[1m0\033[0m")
)
print(f"\n{r = }")


# @functools.cache
# def least_weight_distance(start: Tuple[int, int], end: Tuple[int, int], path=()):
#     """Find the least weight path from the start and end indices of the array.

#     The weight to a node in the array is given by the value at that index."""
#     path = path + (start,)
#     # print(start)
#     if start == end:
#         return 1
#     return sum(
#         least_weight_distance(node, end, path)
#         for node in neighbours(start)
#         if node not in path
#     )


# res = least_weight_distance((0, 0), (9, 9))
# print(res)
# node_distances = defaultdict(lambda: np.inf, {(0, 0): 0})
# visited_nodes = set()
# nodes_to_vist = deque([(0, 0)])

# while nodes_to_vist:
#     node = nodes_to_vist.popleft()
#     neighbours = get_neighbours(node)
#     nodes_to_vist.extend([n for n in neighbours if n not in visited_nodes])
#     visited_nodes.add(node)
#     for n in neighbours:
#         node_distances[n] = min([arr[n] + node_distances[node], node_distances[n]])

# print(node_distances[arr.shape[0] - 1, arr.shape[1] - 1])

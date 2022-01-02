import numpy as np

EMPTY = 0
EAST = 1
SOUTH = 2

table = str.maketrans({".": str(EMPTY), ">": str(EAST), "v": str(SOUTH)})

with open("i") as f:
    data = f.read().translate(table)
lst = [[int(j) for j in line] for line in data.splitlines()]
arr = np.array(lst, dtype=np.uint8)


def step(arr: np.ndarray):
    rolling_east = (arr == EAST) & np.roll(arr == EMPTY, -1, axis=1)
    arr[rolling_east] = EMPTY
    arr[np.roll(rolling_east, 1, axis=1)] = EAST

    rolling_south = (arr == SOUTH) & np.roll(arr == EMPTY, -1, axis=0)
    arr[rolling_south] = EMPTY
    arr[np.roll(rolling_south, 1, axis=0)] = SOUTH

    return (rolling_east | rolling_south).any()


reverse_table = str.maketrans(
    {str(EMPTY): ".", str(EAST): ">", str(SOUTH): "v", " ": "", "[": "", "]": ""}
)


def reconstruct(arr: np.ndarray):
    return str(arr).translate(reverse_table)


print(sum(iter(lambda: step(arr), False)) + 1)

import numpy as np
from numpy.lib.arraysetops import unique
from skimage.segmentation import flood_fill, watershed

with open("i") as f:
    arr = np.array([list(map(int, line.strip())) for line in f], dtype=int)
new = np.ones_like(arr)
new[:-1] *= arr[:-1] < arr[1:]
new[1:] *= arr[1:] < arr[:-1]
new[:, :-1] *= arr[:, :-1] < arr[:, 1:]
new[:, 1:] *= arr[:, 1:] < arr[:, :-1]
result = (arr * new).sum() + new.sum()
print(result)
# print(*np.gradient(arr), sep="\n" + "-" * 50 + "\n")

arr[arr < 9] = 0


# def get_regions(a=arr, value=10, coord=iter(np.argwhere(new).tolist())):
#     """Recursively fill all areas in the array containing 0s with a different colour.
#     The points to flood_fill from are give as a boolean mask in the array called `new`.

#     Parameters
#     ----------
#     arr : array
#         The array to fill
#         value : int
#             The value to fill with
#     """
#     c = next(coord)
#     print(a)
#     print(c)
#     print(value)
#     flooded_arr = flood_fill(a, c, value, connectivity=1)
#     return (
#         a
#         if np.unique(a) == np.unique(flooded_arr)
#         else get_regions(flooded_arr, value + 1)
#     )

s = watershed(arr, connectivity=1) * (arr < 9).astype(int)
unique_, counts = np.unique(s, return_counts=True)
print(np.prod(np.sort(counts[unique_ != 0])[-3:]))
# print(arr)
# print(get_regions())

import skimage.segmentation as s

u, c = np.unique(
    s.watershed(a := np.array([*map(list, open("i").read().split())], dtype=int))
    * (a < 9).astype(int),
    return_counts=True,
)
print(np.prod(np.sort(c[u != 0])[-3:]))
import skimage.segmentation as s

u, c = np.unique(
    s.watershed(a := np.array([*map(list, open("i").read().split())], dtype=int))
    * (a < 9).astype(int),
    return_counts=True,
)
print(np.prod(np.sort(c[u != 0])[-3:]))

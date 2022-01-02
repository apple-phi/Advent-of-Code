import re
import numpy as np

with open("i") as f:
    points, commands = f.read().split("\n\n")
    coords = np.array(eval(points.replace("\n", ","))).reshape(-1, 2)
    arr = np.zeros((max(coords[:, 1]) + 1, max(coords[:, 0]) + 1), dtype=int)
    arr[coords.T[1], coords.T[0]] = 1


def fold_along(arr, axis, index):
    if axis == "y":
        if arr[:index].shape[0] > arr[index:].shape[0]:
            new = arr[:index]
            new[-arr.shape[0] + index :] += arr[1 + index :][::-1]
        else:
            new = arr[1 + index :][::-1]
            new[-index:] += arr[:index]
    elif axis == "x":
        if arr[:, :index].shape[1] > arr[:, 1 + index :].shape[1]:
            new = arr[:, :index]
            new[:, -arr.shape[1] + index :] += arr[:, 1 + index :][:, ::-1]
        else:
            new = arr[:, 1 + index :][:, ::-1]
            new[:, -index:] += arr[:, :index]
    return new


for axis, index in re.findall(r"([x,y])=(\d+)", commands):
    print(axis, index, arr.shape)
    arr = fold_along(arr, axis, int(index))
# print(arr.astype(bool).sum())
for line in arr.astype(bool):
    print("".join(["█" if x else " " for x in line]))

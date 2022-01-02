import numpy as np

with open("tmp") as f:
    data = np.array([list(map(int, i.strip())) for i in f])
# modes = (data.sum(0) > len(data) // 2).astype(int)
# gamma = "".join(modes.astype(str))
# epsilon = "".join((1 - modes).astype(str))
# # print(gamma, epsilon)
# print(int(gamma, 2) * int(epsilon, 2))


def oxy(arr, col=0):
    if len(arr) == 1:
        return arr[0]
    col_sum = arr[:, col].sum()
    mode = 1 if col_sum == len(arr) / 2 else col_sum > len(arr) // 2
    return oxy(arr[arr[:, col] == mode], col + 1)


def co2(arr, col=0):
    if len(arr) == 1:
        return arr[0]
    col_sum = arr[:, col].sum()
    mode = 0 if col_sum == len(arr) / 2 else col_sum <= len(arr) / 2
    return co2(arr[arr[:, col] == mode], col + 1)


print(int("".join(oxy(data).astype(str)), 2) * int("".join(co2(data).astype(str)), 2))
# print(co2(data))

import numpy as np

with open("i") as f:
    arr = np.array([list(map(int, line)) for line in f.read().splitlines()], dtype=int)


def step(arr):
    # print("++++++++++++++++")
    # print(
    #     str(arr)
    #     .replace("[", "")
    #     .replace("]", "")
    #     .replace(" ", "")
    #     .replace("0", "\033[1m0\033[0m")
    # )
    arr += 1
    while (mask := (arr > 9)).any():
        # print("--------------------------------")
        # print(mask)
        arr[:-1] += mask[1:]
        arr[1:] += mask[:-1]
        arr[:, :-1] += mask[:, 1:]
        arr[:, 1:] += mask[:, :-1]
        arr[1:, 1:] += mask[:-1, :-1]
        arr[:-1, :-1] += mask[1:, 1:]
        arr[:-1, 1:] += mask[1:, :-1]
        arr[1:, :-1] += mask[:-1, 1:]
        arr[mask] = -9999
    flashes = (arr < 0).sum()
    arr[arr < 0] = 0
    return flashes


# total_flashes = sum(step(arr) for _ in range(100))
# print(total_flashes)

for i in range(1000):
    if step(arr) == arr.size:
        print(i + 1)
        break

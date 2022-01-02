import numpy as np

with open("i") as f:
    arr = np.array([int(x) for x in f])

print("Part 1:", (arr[1:] > arr[:-1]).sum())

three_at_a_time = np.lib.stride_tricks.sliding_window_view(arr, (3,)).sum(axis=-1)
print("Part 2:", (three_at_a_time[1:] > three_at_a_time[:-1]).sum())

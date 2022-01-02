# with open("i") as f:
#     fishies = list(eval(f.read()))
# # print(*fishies, sep=",")
# for day in range(80):
#     new_fishies = fishies[:]
#     for i, fish in enumerate(fishies):
#         if not fish:
#             new_fishies.append(8)
#             new_fishies[i] = 6
#         else:
#             new_fishies[i] -= 1
#     fishies = new_fishies
#     # print(*fishies, sep=",")
# print(len(fishies))

import numpy as np

with open("i") as f:
    a = np.bincount(eval(f.read()), None, 9)
for _ in range(256):
    a = np.roll(a, -1)
    a[6] += a[8]
print(a.sum())

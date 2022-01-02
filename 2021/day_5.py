import ast
from collections import defaultdict
import numpy as np

lines = []
with open("tmp") as f:
    for line in f:
        lines.append(tuple(ast.literal_eval(p) for p in line.strip().split(" -> ")))

points = defaultdict(int)
for p1, p2 in lines:
    if p1[0] == p2[0]:
        # print("vertical")
        for p in range(p1[1], p2[1] + 1) or range(p2[1], p1[1] + 1):
            points[(p1[0], p)] += 1
    elif p1[1] == p2[1]:
        # print("horizontal")
        for p in range(p1[0], p2[0] + 1) or range(p2[0], p1[0] + 1):
            points[(p, p1[1])] += 1
    # else:
    #     # print("45°")
    #     print(p1, p2)
    #     for x, y in zip(
    #         range(p1[0], p2[0] + 1) or range(p2[0], p1[0] + 1),
    #         range(p1[1], p2[1] + 1) or range(p2[1], p1[1] + 1),
    #     ):
    #         points[(x, y)] += 1
    # elif p1 > p2:
    #     for x, y in zip(
    #         range(p2[0], p1[0] + 1),
    #         range(p1[1], p2[1] + 1) or range(p2[1], p1[1] + 1),
    #     ):
    #         points[(x, y)] += 1
    # elif p2 > p1:
    #     for x, y in zip(
    #         range(p1[0], p2[0] + 1),
    #         range(p1[1], p2[1] + 1) or range(p2[1], p1[1] + 1),
    #     ):
    #         points[(x, y)] += 1
    elif p1[0] > p2[0] and p1[1] > p2[1]:
        for x, y in zip(
            range(p2[0], p1[0] + 1),
            range(p2[1], p1[1] + 1),
        ):
            points[(x, y)] += 1
    elif p1[0] < p2[0] and p1[1] < p2[1]:
        for x, y in zip(
            range(p1[0], p2[0] + 1),
            range(p1[1], p2[1] + 1),
        ):
            points[(x, y)] += 1

    elif p1[0] > p2[0] and p1[1] < p2[1]:
        for x, y in zip(
            range(p2[0], p1[0] + 1),
            range(p2[1], p1[1] - 1, -1),
        ):
            points[(x, y)] += 1
    elif p1[0] < p2[0] and p1[1] > p2[1]:
        for x, y in zip(
            range(p1[0], p2[0] + 1),
            range(p1[1], p2[1] - 1, -1),
        ):
            points[(x, y)] += 1
    else:
        x_range = range(p1[0], p2[0] + 1) or range(p2[0], p1[0] + 1)
        y_range = range(p1[1], p2[1] + 1) or range(p2[1], p1[1] + 1)
        print(p1, p2, x_range, y_range)
        for x, y in zip(x_range, y_range):
            points[(x, y)] += 1


print((np.array(list(points.values())) > 1).sum())
# print()
# a = np.zeros((10, 10))
# for p, c in points.items():
#     if c > 0:
#         a[p[1], p[0]] = c
# for row in a:
#     print(*(str(int(i)) if "0" not in str(int(i)) else "." for i in row), sep="")

print("----")
e, k, l = abs, {}, {}
for a, c, b, d in [eval(_.replace("->", ",")) for _ in open("tmp")]:
    # print(a, b, c, d, sep=" | ")
    for i in range(max(e(g := b - a), e(h := d - c)) + 1):
        l[(z := (x, y))] = (
            l.get(
                (
                    (x := a + i * ((g > 0) - (g < 0))),
                    (y := c + i * ((h > 0) - (h < 0))),
                ),
                0,
            )
            + 1
        )
        if e(g) * e(h) == 0:
            k[z] = k.get(z, 0) + 1
print((o := lambda s: sum(v > 1 for v in s.values()))(k), o(l))

import numpy

m, z = map, numpy.zeros(2 * [999])
for _ in open("tmp"):
    x, y, c, u = eval(_.replace("->", ","))
    d, f = m(numpy.sign, (c - x, u - y))
    while (x, y) != (c + d, u + f):
        z[x][y] += 1
        x, y = x + d, y + f
print(sum(z > 1))

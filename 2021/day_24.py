import re
from typing import *


# def func_block(w, z, a, b, c):
#     x = z % 26 + b != w
#     y = (w + c) * x
#     z = int(z / a) * (25 * x + 1) + y
#     return z


# def forwards(w, z, a, b, c):
#     """Action taken by a single block."""
#     # a is 1 or 26
#     x = z % 26 + b != w
#     return int(z / a) * (25 * x + 1) + (w + c) * x

# re
# def backwards(w, z, a, b, c):
#     """The possible values of z before a given block."""
#     zs = []
#     x = z - w - b
#     if 0 <= w - a < 26:
#         zs.append(w - a + z * c)
#     if x % 26 == 0:
#         zs.append(x // 26 * c)
#     return zs


# test = 5, 0, 1, 12, 1
# f = forwards(*test)
# b = backwards(f, test[0], *test[2:])
# print(f, b)

regex = r"""inp w
mul x 0
add x z
mod x 26
div z (\d+)
add x (-?\d+)
eql x w
eql x 0
mul y 0
add y 25
mul y x
add y 1
mul z y
mul y 0
add y w
add y (\d+)
mul y x
add z y"""
with open("i") as f:
    blocks = [[*map(int, x)] for x in re.findall(regex, f.read())]


def solve(digits: List[str]):
    """Find solution closest to input digits."""
    stack = []
    for block, (div, add_A, add_B) in enumerate(blocks):
        if div == 1:
            stack.append((block, add_B))
        elif div == 26:
            popped_block, popped_add = stack.pop()
            digits[block] = digits[popped_block] + popped_add + add_A
            if digits[block] > 9:
                digits[popped_block] += 9 - digits[block]
                digits[block] = 9
            if digits[block] < 1:
                digits[popped_block] += 1 - digits[block]
                digits[block] = 1
    return "".join(map(str, digits))


print(f"Part 1: {solve([9]*14)}")
print(f"Part 2: {solve([1]*14)}")

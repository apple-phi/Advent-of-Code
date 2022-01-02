import re
import math
import itertools

i = "target area: x=241..273, y=-97..-63"
x_min, x_max, y_min, y_max = map(
    int, re.findall(r"x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)", i)[0]
)

print(y_min * (y_min + 1) // 2)

lowest_dx = int(math.sqrt(2 * x_min))
possibilities = itertools.product(range(lowest_dx, x_max + 1), range(y_min, abs(y_min)))



def does_it_work(dx, dy):
    x = y = 0

    while not (
        y < y_min
        and dy <= 0
        or dx >= 0
        and x > x_max
        or dx <= 0
        and x < x_min
        or dx == 0
        and not x_min <= x <= x_max
    ):
        x += dx
        y += dy

        if dx != 0:
            dx -= abs(dx) / dx
        dy -= 1

        if x_min <= x <= x_max and y_min <= y <= y_max:
            return True

    return False

count = sum(itertools.starmap(does_it_work, possibilities))
print(count)


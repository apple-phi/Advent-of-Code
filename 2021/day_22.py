import re
import math
import dataclasses
import numpy as np


# part 1
with open("p1_area.txt") as f:
    p1_data = f.read().splitlines()

arr = np.zeros((1000,) * 3, dtype=np.int8)
for line in p1_data:
    state, x0, x1, y0, y1, z0, z1 = re.findall(
        r"(off|on) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)", line
    )[0]
    x0, x1, y0, y1, z0, z1 = map(lambda a: int(a) + 200, (x0, x1, y0, y1, z0, z1))
    arr[x0 : x1 + 1, y0 : y1 + 1, z0 : z1 + 1] = state == "on"
print(arr.sum())

# part 2
@dataclasses.dataclass
class Cuboid:
    on: bool
    x_min: int
    x_max: int
    y_min: int
    y_max: int
    z_min: int
    z_max: int

    @property
    def boundaries(self):
        return (
            (self.x_min, self.x_max),
            (self.y_min, self.y_max),
            (self.z_min, self.z_max),
        )

    @property
    def volume(self) -> int:
        return math.prod(axis[1] + 1 - axis[0] for axis in self.boundaries)

    @property
    def effective_volume(self) -> int:
        return (self.on * 2 - 1) * self.volume

    def overlaps_with(self, other) -> bool:
        return not any(
            a[0] > b[1] or a[1] < b[0]
            for a, b in zip(self.boundaries, other.boundaries)
        )

    def negative_intersection_with(self, other) -> "Cuboid":
        assert self.overlaps_with(other), "non-overlapping cubes do not intersect."
        return Cuboid(
            not other.on,
            max(self.x_min, other.x_min),
            min(self.x_max, other.x_max),
            max(self.y_min, other.y_min),
            min(self.y_max, other.y_max),
            max(self.z_min, other.z_min),
            min(self.z_max, other.z_max),
        )


cuboids = []
with open("i") as f:
    for c in map(
        lambda x: Cuboid(x[0] == "on", *map(int, x[1:])),
        re.findall(
            r"(off|on) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)",
            f.read(),
        ),
    ):
        cuboids.extend(
            [
                c.negative_intersection_with(other)
                for other in cuboids
                if c.overlaps_with(other)
            ]
        )
        if c.on:
            cuboids.append(c)
res = sum(c.effective_volume for c in cuboids)
print(res)

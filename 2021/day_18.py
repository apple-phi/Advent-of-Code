from typing import Union, List
from collections import namedtuple
from math import floor, ceil
from functools import reduce
import itertools


list_or_int = Union[int, list]


class Snailfish:
    def __init__(self, left: list_or_int, right: list_or_int):
        self.value = [left, right]

    def __add__(self, other: "Snailfish"):
        return Snailfish(self.value, other.value).reduce()

    __radd__ = __add__

    def reduce(self) -> "Snailfish":
        process = True
        while process:
            process = explode_in_place(self.value) or split_in_place(self.value)
        return self

    @property
    def magnitude(self):
        return get_magnitude(self.value)


def get_magnitude(x: list_or_int):
    if isinstance(x, int):
        return x
    return 3 * get_magnitude(x[0]) + 2 * get_magnitude(x[1])


pair_info = namedtuple("pair_info", ["outer", "index", "depth"], defaults=[1])


def setup_q(lst: List[list_or_int]):
    q: Union[list, int, pair_info] = []
    for i in reversed(range(len(lst))):
        q.append(pair_info(lst, i, 1))
    return q


def explode_in_place(lst: List[list_or_int]):
    history = []
    q = setup_q(lst)
    found = False
    while q:
        curr = q.pop()
        value: list_or_int = curr.outer[curr.index]
        if isinstance(value, list) and (curr.depth < 4 or found):
            for i in reversed(range(len(value))):
                q.append(pair_info(value, i, curr.depth + 1))
        else:
            history.append(
                pair_info(curr.outer, curr.index, curr.depth - isinstance(value, int))
            )
        if isinstance(value, list) and curr.depth == 4 and not found:
            found = True
    if not found:
        return False
    for i, item in enumerate(history):
        if item.depth >= 4 and isinstance(item.outer[item.index], list):
            left, right = item.outer[item.index]
            if i > 0:
                history[i - 1].outer[history[i - 1].index] += left
            if i < len(history) - 1:
                history[i + 1].outer[history[i + 1].index] += right
            item.outer[item.index] = 0
            return True
    return False


def split_in_place(lst: List[list_or_int]):
    q = setup_q(lst)
    while q:
        curr = q.pop()
        value: list_or_int = curr.outer[curr.index]
        if isinstance(value, int) and value >= 10:
            curr.outer[curr.index] = [floor(value / 2), ceil(value / 2)]
            return True
        elif isinstance(value, list):
            for i in reversed(range(len(value))):
                q.append(pair_info(value, i, curr.depth + 1))
    return False


def get_snailfish():
    with open("i") as f:
        data = f.readlines()
    return [Snailfish(*eval(x)) for x in data]


# part 1
res = reduce(Snailfish.__add__, get_snailfish())
print(res.magnitude)

# part 2
res_m = max(
    (get_snailfish()[i] + get_snailfish()[j]).magnitude
    for i, j in itertools.permutations(range(len(get_snailfish())), 2)
)
print(res_m)

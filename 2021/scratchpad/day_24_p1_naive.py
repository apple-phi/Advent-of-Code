from typing import *


class CustomDict(dict):
    def __getitem__(self, key):
        if key not in self:
            return int(key)
        return super().__getitem__(key)


def parse_instr(instr: str, *params: str, var_map: dict, input_iter: iter):
    # print(var_map)
    if instr == "inp":
        var_map[params[0]] = int(next(input_iter))
    elif instr == "add":
        var_map[params[0]] = var_map[params[0]] + var_map[params[1]]
    elif instr == "mul":
        var_map[params[0]] = var_map[params[0]] * var_map[params[1]]
    elif instr == "div":
        var_map[params[0]] = int(var_map[params[0]] / var_map[params[1]])
    elif instr == "mod":
        var_map[params[0]] = var_map[params[0]] % var_map[params[1]]
    elif instr == "eql":
        var_map[params[0]] = var_map[params[0]] == var_map[params[1]]
    else:
        raise NotImplementedError(f"Cannot parse instruction `{instr}`")


with open("i") as f:
    data = f.read().splitlines()


def parse_data(data: List[str], model_number: int):
    variables = CustomDict({"w": 0, "x": 0, "y": 0, "z": 0})
    inputs = iter(str(model_number))
    for line in data:
        parse_instr(*line.split(), var_map=variables, input_iter=inputs)
    assert not tuple(inputs)
    return variables


def check_number(data: List[str], model_number: int):
    assert "0" not in str(model_number)
    assert len(str(model_number)) == str(data).count("inp")
    return not parse_data(data, model_number)["z"]


def find_highest_valid(data: List[str], number_range: range) -> int:  # binary search
    # if not len(number_range):
    #     return number_range.start
    # median = int((number_range.stop + number_range.start) / 2)
    # tested_median = int(str(median).replace("0", "1"))  # remove 0s
    # assert tested_median in number_range
    # # print(number_range, tested_median)
    # if check_number(data, tested_median):  # go higher
    #     next_range = range(number_range.start, median)
    # else:  # go lower
    #     next_range = range(median, number_range.stop)
    # return find_highest_valid(data, next_range)
    while number_range:
        median = int((number_range.stop + number_range.start) / 2)
        tested_median = int(str(median).replace("0", "1"))  # remove 0s
        # assert tested_median in number_range
        print(tested_median, check_number(data, tested_median))
        if check_number(data, tested_median):  # go higher
            number_range = range(median + 1, number_range.stop)
        else:  # go lower
            number_range = range(number_range.start, median)
    return tested_median


MODEL_NUM_RANGE = range(10 ** 13, 10 ** 14)


def part1():
    print(find_highest_valid(data, MODEL_NUM_RANGE))


part1()

from typing import *


class CustomDict(dict):
    def __getitem__(self, key):
        if key not in self:
            return int(key)
        return super().__getitem__(key)


def parse_instr(instr: str, *params: str, var_map: dict, input_iter: Iterator):
    if instr == "inp":
        var_map[params[0]] = next(input_iter)
    elif instr == "add":
        var_map[params[0]] = f"({var_map[params[0]]} + {var_map[params[1]]})"
    elif instr == "mul":
        var_map[params[0]] = f"({var_map[params[0]]} * {var_map[params[1]]})"
    elif instr == "div":
        var_map[
            params[0]
        ] = f"(IntegerPart[{var_map[params[0]]} / {var_map[params[1]]}])"
    elif instr == "mod":
        var_map[params[0]] = f"(Mod[{var_map[params[0]]}, {var_map[params[1]]}])"
    elif instr == "eql":
        var_map[params[0]] = "(Piecewise[{{1, %s == %s}}])" % (
            var_map[params[0]],
            var_map[params[1]],
        )
    else:
        raise NotImplementedError(f"Cannot parse instruction `{instr}`")


with open("i") as f:
    data = f.read().splitlines()


def simplify_data(data: List[str]):
    variables = CustomDict({"w": "0", "x": "0", "y": "0", "z": "0"})
    inputs = iter("abcdefghijklmn")
    for line in data:
        print(line)
        parse_instr(*line.split(), var_map=variables, input_iter=inputs)
    assert not tuple(inputs)
    return variables


print(simplify_data(data)["z"])

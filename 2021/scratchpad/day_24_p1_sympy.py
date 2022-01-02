from typing import *
import sympy as sp


class CustomDict(dict):
    def __getitem__(self, key):
        if key not in self:
            return int(key)
        return super().__getitem__(key)


x1 = sp.symbols("x1")
DIV = sp.Piecewise((sp.ceiling(x1), x1 < 0), (sp.floor(x1), x1 > 0), (0, True))

x2, x3 = sp.symbols("x2 x3")
EQL = sp.Piecewise((1, sp.Eq(x2, x3)), (0, True))


def parse_instr(instr: str, *params: str, var_map: dict, input_iter: Iterator):
    if instr == "inp":
        var_map[params[0]] = next(input_iter)
    elif instr == "add":
        var_map[params[0]] = sp.Add(
            var_map[params[0]], var_map[params[1]], evaluate=False
        )
    elif instr == "mul":
        var_map[params[0]] = sp.Mul(
            var_map[params[0]], var_map[params[1]], evaluate=False
        )
    elif instr == "div":
        val = var_map[params[0]] / var_map[params[1]]
        var_map[params[0]] = sp.Piecewise(
            (sp.ceiling(val), val < 0), (sp.floor(val), val > 0), (0, True)
        )
    elif instr == "mod":
        var_map[params[0]] = sp.Mod(
            var_map[params[0]], var_map[params[1]], evaluate=False
        )
    elif instr == "eql":
        var_map[params[0]] = EQL.xreplace(
            {x2: var_map[params[0]], x3: var_map[params[1]]}
        )
    else:
        raise NotImplementedError(f"Cannot parse instruction `{instr}`")


with open("i") as f:
    data = f.read().splitlines()


def simplify_data(data: List[str]):
    variables = CustomDict({"w": 0, "x": 0, "y": 0, "z": 0})
    inputs = iter(sp.symbols("a b c d e f g h i j k l m n"))
    for line in data:
        print(line)
        print(variables["z"])
        parse_instr(*line.split(), var_map=variables, input_iter=inputs)
    assert not tuple(inputs)
    return variables


print(simplify_data(data)["z"])

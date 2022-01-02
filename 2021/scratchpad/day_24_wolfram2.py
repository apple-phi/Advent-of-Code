from typing import *


def simp(s):
    a, b = s.split(" = ")
    return a + " = " + f"Simplify[{b}, Element[{'|'.join('abcdefghijklmn')}, Integers]]"


def conv(instr: str, *params: str, input_iter: Iterator):
    if instr == "inp":
        return f"{params[0]} = {next(input_iter)}"
    if instr == "add":
        return f"{params[0]} = {params[0]} + {params[1]}"
    if instr == "mul":
        return f"{params[0]} = {params[0]} * {params[1]}"
    if instr == "div":
        return f"{params[0]} = IntegerPart[{params[0]} / {params[1]}]"
    if instr == "mod":
        return f"{params[0]} = Mod[{params[0]}, {params[1]}]"
    if instr == "eql":
        return f"{params[0]} = " + "Piecewise[{{1, %s == %s}}]" % (
            params[0],
            params[1],
        )
    raise NotImplementedError(f"Cannot parse instruction `{instr}`")


i = "|".join("abcdefghijklmn")
inputs = iter("abcdefghijklmn")
with open("i") as f:
    lines = [simp(conv(*line.split(), input_iter=inputs)) for line in f]
print(
    """w = 0
x = 0
y = 0
z = 0
"""
    + "\n".join(lines)
)

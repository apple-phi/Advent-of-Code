import re

with open("i") as f:
    data = f.read()


def total(c):
    return sum(map(int, re.findall(fr"{c} (\d+)", data)))


print("Part 1:", total("forward") * (total("down") - total("up")))


aim = depth = pos = 0
for command, value in map(str.split, data.splitlines()):
    value = int(value)
    if command == "down":
        aim += value
    elif command == "up":
        aim -= value
    elif command == "forward":
        pos += value
        depth += aim * value
    else:
        raise ValueError(f"Unknown command: {command!r}")
print("Part 2:", pos * depth)

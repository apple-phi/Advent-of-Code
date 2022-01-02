from enum import Enum
from statistics import median


class OpenToken(Enum):
    def __new__(cls, open_, close, points):
        obj = object.__new__(cls)
        obj._value_ = open_
        obj.close = close
        obj.points = points
        return obj

    ROUND = ("(", ")", 3)
    CURLY = ("[", "]", 57)
    SQUARE = ("{", "}", 1197)
    TRIANGLE = ("<", ">", 25137)


class CloseToken(Enum):
    def __new__(cls, close, open_, points):
        obj = object.__new__(cls)
        obj._value_ = close
        obj.open_ = open_
        obj.points = points
        return obj

    ROUND_INV = (")", "(", 3)
    CURLY_INV = ("]", "[", 57)
    SQUARE_INV = ("}", "{", 1197)
    TRIANGLE_INV = (">", "<", 25137)


points = 0
scores = []
with open("i") as f:
    for line in f:
        open_tokens = []
        for letter in line.strip():
            try:
                open_tokens.append(OpenToken(letter))
            except ValueError:
                opened = open_tokens.pop()
                closed = CloseToken(letter)
                if closed._value_ != opened.close:
                    print(
                        f"Expected {opened.close}, but found {letter} instead. Points: {closed.points}"
                    )
                    points += closed.points
                    break
        else:
            score = 0
            for token in reversed(open_tokens):
                score = (
                    score * 5 + list(OpenToken.__members__.values()).index(token) + 1
                )
            scores.append(score)
print(points)
print(median(scores))

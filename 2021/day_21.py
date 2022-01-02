import itertools
import re
import collections

with open("i") as f:
    p1_start, p2_start = map(int, re.findall(r"\d.+(\d)", f.read()))


def part_one():

    p1_pos = itertools.cycle(range(1, 11))
    p2_pos = itertools.cycle(range(1, 11))

    p1_score = p2_score = 0

    die = itertools.cycle(range(1, 101))
    n_rolls = 0

    for _ in range(p1_start):
        next(p1_pos)
    for _ in range(p2_start):
        next(p2_pos)

    while True:
        # player 1
        n_rolls += 3
        for _ in range(x := (next(die) + next(die) + next(die) - 1)):
            next(p1_pos)
        p1_score += (y := next(p1_pos))
        if p1_score >= 1000:
            break
        # player 2
        n_rolls += 3
        for _ in range(next(die) + next(die) + next(die) - 1):
            next(p2_pos)
        p2_score += next(p2_pos)
        if p2_score >= 1000:
            break
    print(min(p1_score, p2_score) * n_rolls)


def part_two():
    possible_rolls = collections.Counter(
        sum(i) for i in itertools.product(range(1, 4), repeat=3)
    )
    universes = collections.defaultdict(int, {(p1_start, p2_start, 0, 0): 1})
    p1_win = 0
    p2_win = 0

    while universes:
        unis_after_p1 = collections.defaultdict(int)
        for universe, u_number in universes.items():
            for roll, r_count in possible_rolls.items():
                new_pos = (universe[0] + roll - 1) % 10 + 1
                new_score = universe[2] + new_pos
                new_universes = u_number * r_count
                if new_score >= 21:
                    p1_win += new_universes
                else:
                    unis_after_p1[
                        new_pos, universe[1], new_score, universe[3]
                    ] += new_universes
        universes = unis_after_p1
        unis_after_p2 = collections.defaultdict(int)
        for universe, u_number in universes.items():
            for roll, r_count in possible_rolls.items():
                new_pos = (universe[1] + roll - 1) % 10 + 1
                new_score = universe[3] + new_pos
                new_universes = u_number * r_count
                if new_score >= 21:
                    p2_win += new_universes
                else:
                    unis_after_p2[
                        universe[0], new_pos, universe[2], new_score
                    ] += new_universes
        universes = unis_after_p2
    print(p1_win, p2_win)


part_one()
part_two()

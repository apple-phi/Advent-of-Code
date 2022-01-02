import numpy as np

with open("tmp") as f:
    sections = f.read().split("\n\n")
    numbers = np.fromstring(sections[0], dtype=int, sep=",")
    boards = [
        np.stack(
            [
                np.fromstring(",".join(s.split()), dtype=int, sep=",").reshape(5, 5),
                np.zeros((5, 5), dtype=int),
            ]
        )
        for s in sections[1:]
    ]


def won(board):
    return 5 in board[1].sum(0) or 5 in board[1].sum(1)


# part 1
for n in numbers:
    for b in boards:
        b[1][b[0] == n] = 1
        if won(b):
            print(b[0][b[1] == 0].sum() * n)
            print(b)
            exit()

# part 2
# winners = [False]*len(boards)
# for n in numbers:
#     for i,b in enumerate(boards):
#         b[1][b[0] == n] = 1
#         if won(b):
#             winners[i] = True
#             if all(winners):
#                 print(b[0][b[1] == 0].sum() * n)
#                 exit()

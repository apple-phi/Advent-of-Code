from collections import Counter, defaultdict
import more_itertools as mit

with open("i") as f:
    template, mapping = f.read().split("\n\n")
    mapping = dict(x.split(" -> ") for x in mapping.split("\n"))


# def polymerise(template):
#     return (
#         "".join(o for i, j in mit.pairwise(template) for o in [i, mapping[i + j]])
#         + template[-1]
#     )


# for i in range(40):
#     template = polymerise(template)
#     print(f"{i}: {len(template)}")

# c = Counter(template)
# m = c.most_common()
# print(m[0][1] - m[-1][1])


pair_count = defaultdict(int)

for i, j in mit.pairwise(template):
    pair_count[i + j] += 1


def polymerise():
    for (i, j), v in list(pair_count.items()):
        new = mapping[i + j]
        pair_count[i + new] += v
        pair_count[new + j] += v
        pair_count[i + j] -= v


def polymer_length():
    return sum(v for _, v in list(pair_count.items())) + 1


for _ in range(40):
    polymerise()


letter_count = defaultdict(int)
for (i, j), value in pair_count.items():
    letter_count[i] += value
letter_count[template[-1]] += 1

# print(letter_count)
print(max(letter_count.values()) - min(letter_count.values()))

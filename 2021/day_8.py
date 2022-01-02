import numpy as np

u = {2, 4, 3, 7}
c = 0
with open("i") as f:
    for line in f:
        for word in line.split("|")[1].split():
            if len(word) in u:
                # print(word)
                c += 1
print(c)

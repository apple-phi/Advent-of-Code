import numpy as np

with open("i") as f:
    a = np.array(eval(f.read()))
lowest = np.inf
for i in range(a.min(), a.max()):
    d = np.abs(a - i)
    new = np.sum(d * (d + 1) / 2)
    if new < lowest:
        lowest = new
print(lowest)

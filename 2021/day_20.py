import numpy as np
import scipy.ndimage


def enhance(image: np.ndarray, algo: np.ndarray, n: int) -> np.ndarray:
    padded: np.ndarray = np.pad(image, n)
    for _ in range(n):
        padded = algo[
            scipy.ndimage.correlate(padded, 2 ** np.arange(8, -1, -1).reshape(3, 3))
        ]
    return padded


def p(arr):
    print(
        "\n".join(map(str, arr.tolist()))
        .replace("[", "")
        .replace("]", "")
        .replace(" ", "")
        .replace(",", "")
        .replace("0", ".")
        .replace("1", "#")
        .replace("#", "\033[1m#\033[0m")
    )


with open("i") as f:
    data = f.read().splitlines()
    algorithm = np.array([int(c == "#") for c in data[0]])
    image = np.array([[int(c == "#") for c in line] for line in data[2:]])
    image = enhance(image, algorithm, 50)
    p(image)
    print(image.sum())

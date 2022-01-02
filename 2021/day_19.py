from os import times_result
from typing import *
import itertools
import re

import numpy as np
import cv2

# # elemental rotations
# def Rx(theta):
#     c, s = math.cos(theta), math.sin(theta)
#     return np.array(
#         [
#             [1, 0, 0],
#             [0, c, -s],
#             [0, s, c],
#         ],
#         dtype=int,
#     )


# def Ry(theta):
#     c, s = (
#         math.cos(theta),
#         math.sin(theta),
#     )
#     return np.array(
#         [
#             [c, 0, s],
#             [0, 1, 0],
#             [-s, 0, c],
#         ],
#         dtype=int,
#     )


# def Rz(theta):
#     c, s = math.cos(theta), math.sin(theta)
#     return np.array(
#         [
#             [c, -s, 0],
#             [s, c, 0],
#             [0, 0, 1],
#         ],
#         dtype=int,
#     )


# X = {
#     90: Rx(math.pi / 2),
#     180: Rx(math.pi),
#     270: Rx(3 * math.pi / 2),
# }
# Y = {
#     90: Ry(math.pi / 2),
#     180: Ry(math.pi),
#     270: Ry(3 * math.pi / 2),
# }
# Z = {
#     90: Rz(math.pi / 2),
#     180: Rz(math.pi),
#     270: Rz(3 * math.pi / 2),
# }
# CUBE_ROTATIONS = [
#     np.eye(3, dtype=int),
#     Z[90],
#     Z[180],
#     Z[270],
#     X[90],
#     Y[90] @ X[90],
#     Y[180] @ X[90],
#     Y[270] @ X[90],
#     X[180],
#     Z[90] @ X[180],
#     Z[180] @ X[180],
#     Z[270] @ X[180],
#     X[270],
#     Y[90] @ X[270],
#     Y[180] @ X[270],
#     Y[270] @ X[270],
#     Y[90],
#     X[90] @ Y[90],
#     X[180] @ Y[90],
#     X[270] @ Y[90],
#     Y[270],
#     X[90] @ Y[270],
#     X[180] @ Y[270],
#     X[270] @ Y[270],
# ]


class Scanner:
    def __init__(self, coords: np.ndarray, name):
        self.coords = coords
        self.name = name
        self.beacon_distances = np.array(
            list(
                map(
                    set,
                    np.linalg.norm(self.coords[:, None] - self.coords[None], axis=-1),
                )
            )
        )
        self.positions = [np.array([0, 0, 0])]

    def copy(self):
        return Scanner(self.coords.copy(), self.name)

    # @property
    # def rotations(self) -> List[np.ndarray]:
    #     t = self.coords.T
    #     return [(r @ t).T for r in CUBE_ROTATIONS]

    def overlapping_points(self, other: "Scanner") -> Tuple[List[int], List[int]]:
        self_indexes = []
        other_indexes = []
        for (i, dist_set_a), (j, dist_set_b) in itertools.product(
            enumerate(self.beacon_distances), enumerate(other.beacon_distances)
        ):
            if len(dist_set_a & dist_set_b) >= 12:  # found 12 common points!
                self_indexes.append(i)
                other_indexes.append(j)
                if len(self_indexes) >= 4:  # only need 4 points for Affine transform
                    return self_indexes, other_indexes
        return None, None

    def combine(
        self, other: "Scanner", self_indexes: List[int], other_indexes: List[int]
    ):
        # https://docs.opencv.org/3.4/d9/d0c/group__calib3d.html#ga396afb6411b30770e56ab69548724715
        affine_result = cv2.estimateAffine3D(
            other.coords[other_indexes], self.coords[self_indexes]
        )
        affine_mat = affine_result[1].round().astype(int)
        rotation, translation = affine_mat[:, :3], affine_mat[:, 3]
        transformed = (
            other.coords @ rotation.T + translation
        )  # <=> (rot @ coords.T).T + trans
        premask = (self.coords[:, None] == transformed[None]).all(axis=-1)
        a_equals_b, b_equals_a = np.where(premask)
        not_b_equals_a_mask = ~premask.any(axis=0)
        self.beacon_distances[a_equals_b] |= other.beacon_distances[b_equals_a]
        self.beacon_distances = np.concatenate(
            (self.beacon_distances, other.beacon_distances[not_b_equals_a_mask])
        )
        self.coords = np.concatenate((self.coords, transformed[not_b_equals_a_mask]))
        self.positions.append(translation)

    def combines_with(self, other: "Scanner") -> bool:
        self_indexes, other_indexes = self.overlapping_points(other)
        if self_indexes is None:
            return False
        self.combine(other, self_indexes, other_indexes)
        print(f"{self.name} combined with {other.name}.")
        return True


with open("i") as f:
    data = f.read()
    scanners = [
        Scanner(np.array([eval(c) for c in coords.strip().splitlines()]), name)
        for coords, name in zip(
            re.split(r"--- scanner \d+ ---", data)[1:],
            map(int, re.findall(r"--- scanner (\d+) ---", data)),
        )
    ]

s0 = scanners[0]
unpaired = scanners[1:]
while unpaired:
    unpaired = [s for s in unpaired if not s0.combines_with(s)]

print("Part 1:", len(s0.coords))

scanner_positions = np.asarray(s0.positions)
scanner_distances = np.abs(scanner_positions[:, None] - scanner_positions[None]).sum(axis=-1)
print("Part 2:", scanner_distances.max())

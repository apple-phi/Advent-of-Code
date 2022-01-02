# ridiculously slow (had to leave overnight!!); in future should use complex numbers to model graph instead of strings

from collections import namedtuple, defaultdict
import functools
import math
import heapq
import itertools

graph = {
    "h1": {"h2"},
    "h2": {"h1", "h3"},
    "h3": {"h2", "rA0", "h4"},
    "rA0": {"h3", "rA1"},
    "rA1": {"rA0"},
    "h4": {"h3", "h5"},
    "h5": {"h4", "rB0", "h6"},
    "rB0": {"h5", "rB1"},
    "rB1": {"rB0"},
    "h6": {"h5", "h7"},
    "h7": {"h6", "rC0", "h8"},
    "rC0": {"h7", "rC1"},
    "rC1": {"rC0"},
    "h8": {"h7", "h9"},
    "h9": {"h8", "rD0", "h10"},
    "rD0": {"h9", "rD1"},
    "rD1": {"rD0"},
    "h10": {"h9", "h11"},
    "h11": {"h10"},
}

burrows_by_type = {
    "A": ["rA0", "rA1"],
    "B": ["rB0", "rB1"],
    "C": ["rC0", "rC1"],
    "D": ["rD0", "rD1"],
}


# confirm graph is correct:
def display_graph(graph):
    import networkx as nx

    G = nx.DiGraph()
    for m, conn in graph.items():
        for n in conn:
            G.add_edge(m, n)
    import matplotlib.pyplot as plt

    nx.draw(G, with_labels=True)
    plt.show()


energy_map = {"A": 1, "B": 10, "C": 100, "D": 1000}


def positions_from_pod_info(pod_info: frozenset) -> frozenset:
    return frozenset(list(zip(*pod_info))[1])


def _all_poss_moves(
    curr_pos: str,
    all_positions: frozenset,
    *,
    _found: dict = {},
    _first: bool = True,
    _depth: int = 0
) -> dict:
    if curr_pos in (*all_positions, *_found) and not _first:
        return {}
    _found = {**_found, curr_pos: _depth}
    for pos in graph[curr_pos]:
        if pos not in _found:
            _found = {
                **_found,
                **_all_poss_moves(
                    pos,
                    all_positions,
                    _found=_found,
                    _first=False,
                    _depth=_depth + 1,
                ),
            }
    if _first:
        _found.pop(curr_pos)
    return _found


@functools.lru_cache
def all_poss_moves(curr_pos: str, all_positions: frozenset) -> dict:
    return _all_poss_moves(curr_pos, all_positions)


@functools.lru_cache
# @profile
def get_legal_moves(amphipod: tuple, state: frozenset) -> dict:
    # sourcery skip: comprehension-to-generator

    # final position; don't move (this burrow and lower all filled correctly)
    burrows_for_this_type = burrows_by_type[amphipod[0]]
    if (
        amphipod[1] in burrows_for_this_type
        and {
            (amphipod[0], pos)
            for pos in burrows_for_this_type[burrows_for_this_type.index(amphipod[1]) :]
        }
        <= state
    ):
        return {}

    state_positions = positions_from_pod_info(state)
    found = all_poss_moves(amphipod[1], state_positions)

    found = {
        k: found[k]
        for k in found.keys()
        - {
            "h9",
            "h7",
            "h5",
            "h3",
        }  # never stop on the space immediately outside any room
        - {
            *itertools.chain.from_iterable(
                v for k, v in burrows_by_type.items() if k != amphipod[0]
            )
        }  # remove rooms where it doesn't belong
    }

    # never move from the hallway into a room
    # unless that room is their destination room and
    # that room contains no amphipods which do not also have that room as their own destination
    # happy_room = {"A": True, "B": True, "C": True, "D": True}
    # for amphipod_type, pos in state:
    #     if pos[0] == "r":
    #         occupied_room = pos[1]
    #         if occupied_room != amphipod_type:
    #             happy_room[occupied_room] = False
    # for move_pos in tuple(found.keys()):
    #     if move_pos[0] == "r" and (
    #         not happy_room[move_pos[1]] or move_pos[1] != amphipod[0]
    #     ):
    #         del found[move_pos]

    # go to ideal position if possible
    if not any(
        [
            amphipod_type != amphipod[0] and pos[1] == amphipod[0]
            for amphipod_type, pos in state
        ]
    ):
        allowed_moves_into_rooms = {
            move: depth
            for move, depth in found.items()
            if move[0] == "r" and move[1] == amphipod[0]
        }
        if allowed_moves_into_rooms:
            move, depth = max(allowed_moves_into_rooms.items(), key=lambda x: x[1])
            return {move: depth}
    found = {
        k: found[k] for k in found.keys() - set(burrows_for_this_type)
    }  # otherwise don't go into room

    # Once an amphipod stops moving in the hallway,
    # it will stay in that spot until it can move into a room
    if amphipod[1][0] == "h":
        found = {
            k: found[k]
            for k in found.keys() - {"h1", "h2", "h4", "h6", "h8", "h10", "h11"}
        }

    # # if you can burrow all the way, do it
    # full_burrow = "r" + amphipod[0] + "1"
    # if full_burrow in found:
    #     print("wpp")
    #     return {full_burrow: found[full_burrow]}

    # # if you can complete a burrow, do it
    # top_burrow = "r" + amphipod[0] + "0"
    # if (amphipod[0], full_burrow) in state and top_burrow in found:
    #     return {top_burrow: found[top_burrow]}
    return found


# print(all_poss_moves("h2", positions_from_pod_info(input_state)))
# print(get_legal_moves(("A", "rC0"), frozenset(input_state)))


@functools.lru_cache
# @profile
def poss_state_energy_pairs(state: frozenset) -> list:
    return [
        (
            (state - {amphipod}) | {(amphipod[0], pos)},  # state
            distance * energy_map[amphipod[0]],  # energy
        )
        for amphipod in state
        for pos, distance in get_legal_moves(amphipod, state).items()
    ]


@functools.lru_cache
def move_distance(curr_pos: str, end_pos: str, *, _visited=(), _depth=0):
    if curr_pos == end_pos:
        return _depth
    depths = []
    for pos in graph[curr_pos]:
        if pos not in _visited:
            _visited = _visited + (pos,)
            depths.append(
                move_distance(pos, end_pos, _visited=_visited, _depth=_depth + 1)
            )
    return min(depths) if depths else float("inf")


def set_distances():
    global distance_lookup
    distance_lookup = {
        (start, end): move_distance(
            start,
            end,
        )
        for start, end in itertools.product(graph, repeat=2)
    }


set_distances()


@functools.lru_cache
def heuristic(state: frozenset):  # sourcery skip: comprehension-to-generator
    return sum(
        [
            min(
                [
                    distance_lookup[pos, burrow]
                    for burrow in burrows_by_type[amphipod_type]
                ]
            )
            * energy_map[amphipod_type]
            for amphipod_type, pos in state
        ]
    )


Node = namedtuple("Node", ["f", "state"])

# @profile
def a_star_dist(start_state: frozenset, end_state: frozenset):
    """A* algorithm to calculate minimum energy needed to traverse the given states."""
    start_node = Node(0, start_state)
    open_pq = [start_node]
    g_scores = defaultdict(lambda: math.inf)
    g_scores[start_state] = 0
    while open_pq:
        curr_node = heapq.heappop(open_pq)
        if curr_node.state == end_state:  # end node
            return g_scores[end_state]
        for state, energy in poss_state_energy_pairs(curr_node.state):
            g = g_scores[curr_node.state] + energy
            if g < g_scores[state]:  # new best
                g_scores[state] = g
                h = heuristic(state)
                f = g + h
                child_node = Node(f, state)
                heapq.heappush(open_pq, child_node)
    return "No solution found."


def part1():
    input_state = {
        ("A", "rC1"),
        ("A", "rD1"),
        ("B", "rA1"),
        ("B", "rB0"),
        ("C", "rB1"),
        ("C", "rA0"),
        ("D", "rC0"),
        ("D", "rD0"),
    }
    # test input
    # input_state = {
    #     ("A", "rA1"),
    #     ("A", "rD1"),
    #     ("B", "rA0"),
    #     ("B", "rC0"),
    #     ("C", "rC1"),
    #     ("C", "rB0"),
    #     ("D", "rD0"),
    #     ("D", "rB1"),
    # }

    # debug input
    # input_state = {
    #     ("A", "rD0"),
    #     ("A", "rD1"),
    #     ("B", "rA0"),
    #     ("B", "rB1"),
    #     ("C", "rC0"),
    #     ("C", "rC1"),
    #     ("D", "rB0"),
    #     ("D", "rA1"),
    # }

    ideal_state = {
        ("A", "rA0"),
        ("A", "rA1"),
        ("B", "rB0"),
        ("B", "rB1"),
        ("C", "rC0"),
        ("C", "rC1"),
        ("D", "rD0"),
        ("D", "rD1"),
    }
    print("Lower bound to result:", heuristic(frozenset(input_state)))
    print(a_star_dist(frozenset(input_state), frozenset(ideal_state)))


def part2():
    global graph, burrows_by_type
    graph = {
        "h1": {"h2"},
        "h2": {"h1", "h3"},
        "h3": {"h2", "rA0", "h4"},
        "rA0": {"h3", "rA1"},
        "rA1": {"rA0", "rA2"},
        "rA2": {"rA1", "rA3"},
        "rA3": {"rA2"},
        "h4": {"h3", "h5"},
        "h5": {"h4", "rB0", "h6"},
        "rB0": {"h5", "rB1"},
        "rB1": {"rB0", "rB2"},
        "rB2": {"rB1", "rB3"},
        "rB3": {"rB2"},
        "h6": {"h5", "h7"},
        "h7": {"h6", "rC0", "h8"},
        "rC0": {"h7", "rC1"},
        "rC1": {"rC0", "rC2"},
        "rC2": {"rC1", "rC3"},
        "rC3": {"rC2"},
        "h8": {"h7", "h9"},
        "h9": {"h8", "rD0", "h10"},
        "rD0": {"h9", "rD1"},
        "rD1": {"rD0", "rD2"},
        "rD2": {"rD1", "rD3"},
        "rD3": {"rD2"},
        "h10": {"h9", "h11"},
        "h11": {"h10"},
    }
    set_distances()
    burrows_by_type = {
        "A": ["rA0", "rA1", "rA2", "rA3"],
        "B": ["rB0", "rB1", "rB2", "rB3"],
        "C": ["rC0", "rC1", "rC2", "rC3"],
        "D": ["rD0", "rD1", "rD2", "rD3"],
    }
    input_state = {
        ("A", "rC3"),
        ("A", "rD3"),
        ("B", "rA3"),
        ("B", "rB0"),
        ("C", "rB3"),
        ("C", "rA0"),
        ("D", "rC0"),
        ("D", "rD0"),
    }
    extra_lines = {
        ("A", "rD1"),
        ("A", "rC2"),
        ("B", "rB2"),
        ("B", "rC1"),
        ("C", "rB1"),
        ("C", "rD2"),
        ("D", "rA1"),
        ("D", "rA2"),
    }
    input_state |= extra_lines
    # input_state = {
    #     ("A", "rA0"),
    #     ("A", "rA1"),
    #     ("A", "rA2"),
    #     ("A", "rA3"),
    #     ("B", "rB0"),
    #     ("B", "rB1"),
    #     ("B", "rB2"),
    #     ("B", "rB3"),
    #     ("C", "h8"),
    #     ("C", "rC1"),
    #     ("C", "rC2"),
    #     ("C", "rC3"),
    #     ("D", "rD0"),
    #     ("D", "rD1"),
    #     ("D", "rD2"),
    #     ("D", "rD3"),
    # }

    ideal_state = {
        ("A", "rA0"),
        ("A", "rA1"),
        ("A", "rA2"),
        ("A", "rA3"),
        ("B", "rB0"),
        ("B", "rB1"),
        ("B", "rB2"),
        ("B", "rB3"),
        ("C", "rC0"),
        ("C", "rC1"),
        ("C", "rC2"),
        ("C", "rC3"),
        ("D", "rD0"),
        ("D", "rD1"),
        ("D", "rD2"),
        ("D", "rD3"),
    }
    print("Lower bound to result:", heuristic(frozenset(input_state)))
    print(get_legal_moves(("C", "rC1"), frozenset(input_state)))
    print(a_star_dist(frozenset(input_state), frozenset(ideal_state)))


part1()
part2()

from collections import defaultdict

graph = defaultdict(set)
with open("i") as f:
    for line in f:
        a, b = line.strip().split("-")
        graph[a].add(b)
        graph[b].add(a)


def count_all_paths_p1(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return 1
    if start not in graph:
        return 0
    return sum(
        count_all_paths_p1(graph, node, end, path)
        for node in graph[start]
        if node.isupper() or node not in path
    )


print(count_all_paths_p1(graph, "start", "end"))


def count_all_paths_p2(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return 1
    if start not in graph:
        return 0
    return sum(
        count_all_paths_p2(graph, node, end, path)
        for node in graph[start]
        if node != "start"
        and (
            node.isupper()
            or node not in path
            or sum(n.islower() for n in path) == len({n for n in path if n.islower()})
        )
    )


print(count_all_paths_p2(graph, "start", "end"))

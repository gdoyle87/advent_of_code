import math
from collections import namedtuple

from utils.loader import load_lines

Point = namedtuple("Point", ["x", "y", "z"])
Edge = namedtuple("Edge", ["distance", "i", "j"])
Data = namedtuple("Data", ["points", "edges", "n"])

CONNECTIONS_NEEDED = 1000


def part1(data):
    parent = list(range(data.n))  # initialize each as its own parent
    circuit_sizes = [1] * data.n  # each circuit begins as size 1

    def union(i, j):
        def find(i):
            if parent[i] == i:
                return i
            parent[i] = find(parent[i])
            return parent[i]

        root_i = find(i)
        root_j = find(j)

        if root_i != root_j:
            #            if circuit_sizes[root_i] < circuit_sizes[root_j]:
            #                root_i, root_j = root_j, root_i

            # update the parent of j to be parent of i
            parent[root_j] = root_i
            # update the size of circuit i to also include the size of circuit j
            circuit_sizes[root_i] += circuit_sizes[root_j]
            return True
        return False

    # combine edges starting from shortest, stop once we have reached the required number of connections
    connections = 0
    for edge in data.edges:
        union(edge.i, edge.j)
        connections += 1
        if connections == CONNECTIONS_NEEDED:
            break

    # circuit_sizes includes sizes for every point in edges, even when they are not a parent point.
    # Therefore we need to filter out nodes where the circuit is not a parent.
    final_sizes = [circuit_sizes[i] for i in range(data.n) if parent[i] == i]

    # we want only the top 3 size circuits so sort desc
    final_sizes.sort(reverse=True)
    return math.prod(final_sizes[:3])


def part2(data):
    parent = list(range(data.n))  # initialize each as its own parent
    circuit_sizes = [1] * data.n  # each circuit begins as size 1

    def union(i, j):
        def find(i):
            if parent[i] == i:
                return i
            parent[i] = find(parent[i])
            return parent[i]

        root_i = find(i)
        root_j = find(j)

        if root_i != root_j:
            #            if circuit_sizes[root_i] < circuit_sizes[root_j]:
            #                root_i, root_j = root_j, root_i

            # update the parent of j to be parent of i
            parent[root_j] = root_i
            # update the size of circuit i to also include the size of circuit j
            circuit_sizes[root_i] += circuit_sizes[root_j]
            return True
        return False

    # combine edges starting from shortest, stop once we have connected all points (needs n - 1 connections)
    connections = 0
    last_edge = None
    for edge in data.edges:
        if union(edge.i, edge.j):
            connections += 1
            if connections == data.n - 1:
                last_edge = edge
                break

    return data[last_edge.i].x * data[last_edge.j].x


def solve():
    data = load_lines(8)
    points = []
    for point in data:
        x, y, z = map(int, point.split(","))
        points.append(Point(x, y, z))

    n = len(data)

    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            p1, p2 = data[i], data[j]
            distance_sq = (p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2 + (p1.z - p2.z) ** 2
            edges.append(Edge(distance_sq, i, j))
    edges.sort()

    data = Data(points, edges, n)

    return part1(data), part2(data)

from collections import namedtuple

from utils.loader import load_lines

Point = namedtuple("Point", ["x", "y", "z"])
Edge = namedtuple("Edge", ["distance", "i", "j"])


def part1(data):
    n = len(data)

    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            p1, p2 = data[i], data[j]
            distance_sq = (p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2 + (p1.z - p2.z) ** 2
            edges.append(Edge(distance_sq, i, j))
    edges.sort()
    print(edges)
    return


def part2(data):
    pass


def solve():
    data = load_lines(8)
    points = []
    for point in data:
        x, y, z = map(int, point.split(","))
        points.append(Point(x, y, z))

    return part1(points), part2(points)

from collections import namedtuple

from utils.loader import load_lines

Point = namedtuple("Point", ["x", "y"])
Edge = namedtuple("Edge", ["distance", "i", "j"])


def part1(data):
    return data[0].distance


def part2(data):
    pass


def solve():
    data = load_lines(9)
    points = []
    for point in data:
        x, y = map(int, point.split(","))
        points.append(Point(x, y))

    n = len(points)

    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            p1, p2 = points[i], points[j]
            distance = abs(p1.x - p2.x + 1) * abs(p1.y - p2.y + 1)
            edges.append(Edge(distance, i, j))
    edges.sort(reverse=True)

    return part1(edges), part2(data)

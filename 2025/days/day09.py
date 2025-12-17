from collections import namedtuple

from utils.loader import load_lines

Point = namedtuple("Point", ["x", "y"])
Rectangle = namedtuple("Rectangle", ["area", "min_x", "max_x", "min_y", "max_y"])
Edge = namedtuple("Edge", ["p1", "p2"])
Data = namedtuple("Data", ["rectangles", "polygon"])


def part1(data):
    return data.rectangles[0].area


def part2(data):
    def is_inside(edges, x, y):
        for edge in edges:
            print(edge)
            if (y < edge.p1.y) != (y < edge.p2.y):
                print("y is between")
            else:
                print("y is not between")

    is_inside(data.polygon[:2], 1, 1)


def solve():
    data = load_lines(9)
    points = []
    for point in data:
        x, y = map(int, point.split(","))
        points.append(Point(x, y))

    n = len(points)

    rectangles = []
    for i in range(n):
        for j in range(i + 1, n):
            p1, p2 = points[i], points[j]
            min_x, max_x = min(p1.x, p2.x), max(p1.x, p2.x)
            min_y, max_y = min(p1.y, p2.y), max(p1.y, p2.y)
            width = max_x - min_x + 1
            height = max_y - min_y + 1
            area = width * height
            rectangles.append(Rectangle(area, min_x, max_x, min_y, max_y))
    rectangles.sort(reverse=True)

    polygon = []
    for i in range(len(points)):
        p1 = points[i]
        p2 = points[(i + 1) % n]
        polygon.append(Edge(p1, p2))
    data = Data(rectangles, polygon)

    print(polygon[:2])

    return part1(data), part2(data)

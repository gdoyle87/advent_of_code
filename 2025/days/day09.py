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
        cross_count = 0
        for edge in edges:
            if (y < edge.p1.y) != (y < edge.p2.y):
                x_between = edge.p1.x + ((y - edge.p1.y) / (edge.p2.y - edge.p1.y)) * (
                    edge.p2.x - edge.p1.x
                )
                if x < x_between:
                    cross_count += 1
        return cross_count % 2 == 1

    def check_rect(rect):
        for x in range(rect.min_x, rect.max_x + 1):
            for y in range(rect.min_y, rect.max_y + 1):
                if not is_inside(data.polygon, x, y):
                    return False
        return True

    for rectangle in data.rectangles:
        if check_rect(rectangle):
            return rectangle.area


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

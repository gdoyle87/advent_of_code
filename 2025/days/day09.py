from collections import namedtuple

from utils.loader import load_lines

Point = namedtuple("Point", ["x", "y"])
Rectangle = namedtuple("Rectangle", ["area", "min_x", "max_x", "min_y", "max_y"])
Edge = namedtuple("Edge", ["p1", "p2", "etype"])
Data = namedtuple("Data", ["points", "rectangles", "edges", "num_points"])


def part1(data):
    return data.rectangles[0].area


def part2(data):
    def is_point_inside(x, y):
        crossings = 0
        for edge in data.edges:
            # only need to check vertical crossings
            if edge.etype == "same_x":
                low_y, high_y = min(edge.p1.y, edge.p2.y), max(edge.p1.y, edge.p2.y)
                if low_y <= y < high_y and x <= edge.p1.x:
                    crossings += 1
        return crossings % 2 == 1

    for rect in data.rectangles:
        if not is_point_inside(rect.min_x, rect.min_y):
            continue
        rect_crossed = False
        for edge in data.edges:
            if edge.etype == "same_x":
                low, high = min(edge.p1.y, edge.p2.y), max(edge.p1.y, edge.p2.y)
                if rect.min_x < edge.p1.x < rect.max_x:
                    if not (high <= rect.min_y or low >= rect.max_y):
                        rect_crossed = True
                        break
            else:
                low, high = min(edge.p1.x, edge.p2.x), max(edge.p1.x, edge.p2.x)
                if rect.min_y < edge.p1.y < rect.max_y:
                    if not (high <= rect.min_x or low >= rect.max_x):
                        rect_crossed = True
                        break
        if not rect_crossed:
            return rect.area


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

    edges = []
    for i in range(n - 1):
        p1, p2 = points[i], points[i + 1]
        etype = "same_x"
        if p1.y == p2.y:
            etype = "same_y"
        edge = Edge(points[i], points[i + 1], etype)
        edges.append(edge)

    data = Data(points, rectangles, edges, n)
    return part1(data), part2(data)

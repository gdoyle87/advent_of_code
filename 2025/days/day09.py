from collections import namedtuple

from utils.loader import load_lines

Point = namedtuple("Point", ["x", "y"])
Rectangle = namedtuple("Rectangle", ["area", "min_x", "max_x", "min_y", "max_y"])
Edge = namedtuple("Edge", ["p1", "p2"])
Polygon = namedtuple("Polygon", ["v_edges", "min_y", "max_y"])
Data = namedtuple("Data", ["rectangles", "polygon"])


def part1(data):
    return data.rectangles[0].area


def part2(data):
    row_spans = {}
    for y in range(data.polygon.min_y, data.polygon.max_y + 1):
        crossings = sorted(edge.p1.x for edge in data.polygon.v_edges if min(edge.p1.y, edge,p2.y) <= y < max(edge.p1.y, edge.p2.y)])
        
        row_spans[y] = [(crossings[i], crossings[i+1]) for i in range(0,len(crossings), 2)]

    print(row_spans)

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

    vertical_edges = []
    polygon_min_y = points[0].y
    polygon_max_y = points[0].y
    for i in range(len(points)):
        p1 = points[i]
        p2 = points[(i + 1) % n]
        if p1.x == p2.x:
            vertical_edges.append(Edge(p1, p2))
            polygon_min_y = min(polygon_min_y, p1.y, p2.y)
            polygon_max_y = max(polygon_max_y, p1.y, p2.y)
    polygon = Polygon(vertical_edges, polygon_min_y, polygon_max_y)
    data = Data(rectangles, polygon)

    print(polygon[:2])

    return part1(data), part2(data)

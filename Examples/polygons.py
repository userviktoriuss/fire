import math

from shapely import Point, Polygon
from Utils.Circle import Circle
polygons_dict = dict()

# Описание многоугольников, использованных для тестирования

# P1 ----------------------------------------------------------------
P1 = Polygon([Point(0, 0), Point(2, 0), Point(6, 2), Point(1, 5), Point(1, 4)])
polygons_dict['P1'] = P1

# P2 ----------------------------------------------------------------
P2 = Polygon([Point(0, 0), Point(8, 0), Point(8, 2), Point(7, 2), Point(7, 1.5), Point(2, 1.5), Point(2, 2), Point(0, 2)])
polygons_dict['P2'] = P2

# P3 ----------------------------------------------------------------
P3 = Circle(Point(3, 3), radius=3).polygon
polygons_dict['P3'] = P3

# P4 ----------------------------------------------------------------
P4 = Polygon([Point(0, 0), Point(16, 0), Point(15, 2), Point(14, 3), Point(12, 4), Point(4, 4), Point(2, 3), Point(1, 2)])
polygons_dict['P4'] = P4

# P6 ----------------------------------------------------------------
#P6 = Polygon([Point(0, 0), Point(40, 0), Point(40, 40), Point(20, 30), Point(0, 40)])
#polygons_dict['P6'] = P6

# P7 ----------------------------------------------------------------
P7 = Polygon([Point(0, 0), Point(5, 0), Point(5, 4), Point(0, 4)])
holes = [Circle(Point(1.5, 0.5), 0.25).polygon, Circle(Point(3.5, 0.5), 0.25).polygon, Circle(Point(1.5, 3.5), 0.25).polygon, Circle(Point(3.5, 3.5), 0.25).polygon]
for h in holes:
    P7 = P7.difference(h)
polygons_dict['P7'] = P7

# P8 ----------------------------------------------------------------
P8 = Circle(Point(4, 4), 4).polygon.difference(Circle(Point(5, 4), 2).polygon)
polygons_dict['P8'] = P8

# P9 ----------------------------------------------------------------
dx = 1.5
theta = 60
hypot = dx / math.cos(theta)
dy = math.sqrt(hypot ** 2 - dx ** 2)
P9 = Polygon([Point(dx * k / 10, (dx * k / 10) ** 6) for k in range(10)] + [Point(0.5 * dx, (0.9 * dx) ** 6)])
polygons_dict['P9'] = P9


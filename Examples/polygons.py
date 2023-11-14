from shapely import Point, Polygon
from Utils.Circle import Circle
polygons_dict = dict()

# Описание многоугольников


# P8 ----------------------------------------------------------------
P8 = Circle(Point(4, 4), 4).polygon.difference(Circle(Point(5, 4), 2).polygon)
polygons_dict['P8'] = P8
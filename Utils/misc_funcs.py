from itertools import zip_longest

from shapely import Polygon, Point
import random


def point_inside_polygon(polygon: Polygon) -> Point:
    minx, miny, maxx, maxy = polygon.bounds

    while True:
        x = random.uniform(minx, maxx)
        y = random.uniform(miny, maxy)
        p = Point(x, y)
        if polygon.contains(p):
            return p


def group_n(n, iterable, fill_value=None):
    """Вот это мощь питона!"""
    args = [iter(iterable)] * n
    return list(zip_longest(fillvalue=fill_value, *args))


def sign(a: float) -> int:
    """
    Возвращает знак переданного числа:
     0 - a = 0
    -1 - a < 0
     1 - a > 0
    :param a: Переданное число.
    :return: -1/0/1
    """

    if a == 0:
        return 0
    elif a > 0:
        return 1
    return -1

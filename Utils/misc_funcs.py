from itertools import zip_longest

import numpy as np
from shapely import Polygon, Point
import random


def expected_circle_count(P: Polygon, r: float) -> int:
    """
    Вычисляет нижнюю границу количества кругов, необходимых для покрытия P.
    :param P: Заданный многоугольник.
    :return: Оценка на количество кругов, необходимых для покрытия P.
    """
    D = 2 * np.pi / np.sqrt(27)
    per = P.exterior.length + sum(x.length for x in P.interiors)

    inside = P.area * D
    outside = per * np.sqrt(2) * r * (2 * np.pi - 2) / 12
    N = (inside + outside) / (np.pi * r * r)
    N = int(np.ceil(N))
    return N

def expected_circle_count2(P: Polygon, r: float) -> int:
    """
    Вычисляет нижнюю границу количества кругов, необходимых для покрытия P.
    Строится так же, как и первая версия, но берёт в качестве предположения, что P - круг.
    :param P: Заданный многоугольник.
    :return: Оценка на количество кругов, необходимых для покрытия P.
    """
    D = 2 * np.pi / np.sqrt(27)
    per = P.exterior.length + sum(x.length for x in P.interiors)

    inside = P.area * D / (np.pi * r * r)
    outside = (per - np.pi * r) / (r * np.sqrt(3))
    N = inside + outside
    N = int(np.ceil(N))
    return N

def expected_circle_count_weighted(P: Polygon, r: float) -> int:
    """
    Вычисляет нижнюю границу количества кругов, необходимых для покрытия P.
    Взвешивает в пропорции 4:1 первую и вторую оценки.
    :param P: Заданный многоугольник.
    :return: Оценка на количество кругов, необходимых для покрытия P.
    """
    k1 = expected_circle_count(P, r)  # Ожидаемое количество кругов, необходимое для покрытия.
    k2 = expected_circle_count2(P, r)
    k_weighted = int(np.ceil((k1 * 4 + k2) / 5))
    return k_weighted


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

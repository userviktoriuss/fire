# Заполнение путём построения шестиугольной сетки.
# Строит сетку и возвращает центры шестиугольников,
# которые попали внутрь заданного многоугольника
import math

import numpy as np
from shapely import Polygon, Point, LineString

# ------------------------------------------------------------------------------
# Реализация покрытия шестиугольной сеткой с помощью библиотеки Shapely
# ------------------------------------------------------------------------------

def hexagonal(P: Polygon, S: Point, a: float = 1, alpha: float = 0):
    """
    Строит шестиугольную сетку с начальной точкой S, длиной
    стороны шестиугольника равной a и повёрнутой на угол alpha
    относительно O внутри многоугольника P. Возвращает список точек - центры
    шестиугольников, которые попали внутрь многоугольника P.

    :param P: Многоугольник.
    :param S: Стартовая точка.
    :param a: Длина стороны шестиугольников сетки.
    :param alpha: Угол поворота сетки [0; pi/3]
    :return: Центры соответствующих шестиугольников.
    """

    minx, miny, maxx, maxy = P.bounds

    k = S.distance(P.boundary) + 2 * ((maxx - minx) ** 2 + (maxy - miny) ** 2)
    # Буду двигать эти прямые. На каждом пересечении
    # лежит центр многоугольника.
    dif_hor = rotate(Point(3 * a, 0), alpha)

    horizontal = LineString(
        [Point(S.x - k * dif_hor.x, S.y - k * dif_hor.y), Point(S.x + k * dif_hor.x, S.y + k * dif_hor.y)])
    dif_obl = rotate(Point(1.5 * a, math.sqrt(3) * a / 2), alpha)
    oblique = LineString(
        [Point(S.x - k * dif_obl.x, S.y - k * dif_obl.y), Point(S.x + k * dif_obl.x, S.y + k * dif_obl.y)])

    all_hor = get_parallel(P, horizontal, rotate(Point(0, math.sqrt(3) * a / 2), alpha))
    all_obl = get_parallel(P, oblique, rotate(Point(3 * a, 0), alpha))

    ans = []
    for hor in all_hor:
        for obl in all_obl:
            C = hor.intersection(obl)
            if P.contains(C):
                ans.append(C)

    return ans


def get_parallel(P: Polygon, line: LineString, move: Point) -> list[LineString]:
    """
    Находит все сдвиги прямой line на вектор k*move, такие, что
    прямая пересекает Polygon.

    :param P: Многоугольник, с которым ищем пересечения.
    :param line: Прямая, которую двигаем.
    :param move: Вектор сдвига.
    :return: Список прямых LineString, пересекающих Polygon.
    """

    ans = []
    cpy = LineString([c for c in line.coords])  # TODO: правда сохранил, и смогу сходить в др. сторону?

    while not P.intersection(line).is_empty:
        ans.append(line)
        line = LineString([[c[0] + move.x, c[1] + move.y] for c in line.coords])

    line = LineString([[c[0] - move.x, c[1] - move.y] for c in cpy.coords])
    while not P.intersection(line).is_empty:
        ans.append(line)
        line = LineString([[c[0] - move.x, c[1] - move.y] for c in line.coords])

    return ans


def rotate(p: Point, alpha: float):
    """
    Поворачивает точку на угол alpha относительно (0; 0).

    :param p: Точка, которую надо повернуть.
    :param alpha: Угол в радианах, на который надо повернуть.
    :return: Точку после поворота.
    """

    nx = p.x * math.cos(alpha) - p.y * math.sin(alpha)
    ny = p.x * math.sin(alpha) + p.y * math.cos(alpha)

    return Point(nx, ny)


# ------------------------------------------------------------------------------
# Реализация покрытия шестиугольной сеткой с помощью библиотеки Numpy
# ------------------------------------------------------------------------------


def hexagonal_np(P: Polygon, S: Point, a: float = 1, alpha: float = 0):
    rotate = np.array([[np.cos(alpha), -np.sin(alpha)],
                       [np.sin(alpha), np.cos(alpha)]])

    x0 = np.array([S.x, S.y])
    (minx, miny, maxx, maxy) = P.bounds

    minx -= x0[0]
    maxx -= x0[0]
    miny -= x0[1]
    maxy -= x0[1]

    v = rotate @ np.array([3 * a, 0])
    u = rotate @ np.array([3 / 2 * a, a * np.sqrt(3) / 2])

    transition = np.linalg.inv(np.vstack([v, u]).T)

    bounds = transition @ np.array([[minx, maxx, minx, maxx], [miny, maxy, maxy, miny]])

    kminx = np.floor(np.min(bounds[0, :]))
    kmaxx = np.ceil(np.max(bounds[0, :]))
    kminy = np.floor(np.min(bounds[1, :]))
    kmaxy = np.ceil(np.max(bounds[1, :]))

    all_v = (np.arange(kminx, kmaxx + 1) * v.reshape(2, 1)).T
    all_u = (np.arange(kminy, kmaxy + 1) * u.reshape(2, 1)).T

    coverage = all_v[None, :, :] + all_u[:, None, :]

    # Вернём в изначальную систему координат.
    coverage += x0

    (minx, miny, maxx, maxy) = P.bounds
    # Соберём в объекты-точки только те координаты, что могут потенциально пригодиться.
    shape = coverage.shape
    coverage = coverage.reshape(shape[0] * shape[1], shape[2])

    cond = np.logical_and(
        np.logical_and(minx <= coverage[:, 0], coverage[:, 0] <= maxx),
        np.logical_and(miny <= coverage[:, 1], coverage[:, 1] <= maxy))
    useful = coverage[cond]


    to_points = lambda c: Point(c)
    to_points_vectorized = np.vectorize(to_points, signature='(d)->()')

    ans = to_points_vectorized(useful)
    #
    #for i in range(coverage.shape[0]):
    #    for j in range(coverage.shape[1]):
    #        (x, y) = coverage[i, j]
    #        if minx <= x <= maxx and miny <= y <= maxy:
    #            ans.append(Point(x, y))

    return list(ans)
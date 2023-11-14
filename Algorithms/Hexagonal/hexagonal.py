from shapely import Point, Polygon, LineString
import math



# Заполнение путём построения шестиугольной сетки.
# Строит сетку и возвращает центры шестиугольников,
# которые попали внутрь заданного многоугольника

def hexagonal(P: Polygon, S: Point, a: float = 1, alpha: float = 0):
    """
    Строит шестиугольную сетку с начальной точкой S, длиной
    стороны шестиугольника равной a и повёрнутой на угол alpha
    относительно O внутри многоугольника P. Возвращает список точек - центры
    шестиугольников, которые попали внутрь многоугольника P.

    :param P: Многоугольник.
    :param s: Стартовая точка.
    :param a: Длина стороны шестиугольников сетки.
    :param alpha: Угол поворота сетки [0; pi/3]
    :return: Центры соответствующих шестиугольников.
    """

    minx, miny, maxx, maxy = P.bounds

    k = S.distance(P.boundary) + 2 * ((maxx - minx) ** 2 + (maxy - miny) ** 2)
    # Буду двигать эти прямые. На каждом пересечении
    # лежит центр многоугольника.
    dif_hor = rotate(Point(3 * a, 0), alpha)

    horizontal = LineString([Point(S.x - k * dif_hor.x, S.y - k * dif_hor.y), Point(S.x + k * dif_hor.x, S.y + k * dif_hor.y)])
    dif_obl = rotate(Point(1.5 * a, math.sqrt(3) * a / 2), alpha)
    oblique = LineString([Point(S.x - k * dif_obl.x, S.y - k * dif_obl.y), Point(S.x + k * dif_obl.x, S.y + k * dif_obl.y)])

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

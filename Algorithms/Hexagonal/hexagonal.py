from shapely import Point, Polygon, LineString
import math

from shapely.ops import unary_union

from Utils.Circle import Circle


class HexagonalAlgorithm:
    def __init__(self, P: Polygon, radius: float):
        self.P = P
        self.radius = radius
        (minx, miny, maxx, maxy) = P.bounds
        self.P_described = Polygon([Point(minx - radius, miny - radius),
                                    Point(maxx + radius, miny - radius),
                                    Point(maxx + radius, maxy + radius),
                                    Point(minx - radius, maxy + radius)])

    def set_params(self,
                   RESOLUTION: int=5,
                   ALPHA_RESOLUTION: int=5,
                   EPS: float = 1e-3):
        self.RESOLUTION = RESOLUTION
        self.ALPHA_RESOLUTION = ALPHA_RESOLUTION
        self.EPS = EPS

    def run_algorithm(self):
        self.best_ops = (0, 0, 0)
        self.best_val = float('inf')

        step_alpha = math.pi / 3 / self.ALPHA_RESOLUTION
        step_x = self.radius / self.RESOLUTION
        step_y = self.radius / self.RESOLUTION
        alpha = 0
        while alpha < math.pi / 3:
            x = 0
            while x < self.radius:
                y = 0
                while y < self.radius:
                    S = Point(x, y)

                    important = self.get_important(S, alpha)

                    if len(important) < self.best_val:
                        self.best_val = len(important)
                        self.best_ops = (x, y, alpha)
                    y += step_y
                x += step_x
            alpha += step_alpha

    def get_important(self, S, alpha):
        outer_grid = hexagonal(self.P_described, S, self.radius, alpha)

        inside = [Circle(c, 1) for c in outer_grid if self.P.contains(c)]
        outside = [Circle(c, 1) for c in outer_grid if not self.P.contains(c)]
        union = unary_union([c.polygon for c in inside])

        outside.sort(key=
                     lambda c: self.P.intersection(c.polygon).area,
                     reverse=True)
        for c in outside:
            c_inside_polygon = self.P.intersection(c.polygon)
            united = unary_union([union, c_inside_polygon])
            if abs(united.area - union.area) > self.EPS:
                inside.append(c)
                union = unary_union([union, c_inside_polygon])
        return inside

    def get_result(self):
        return self.get_important(Point(self.best_ops[0], self.best_ops[1]), self.best_ops[2])


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

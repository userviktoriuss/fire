from shapely import Polygon, Point
import logging

logger = logging.getLogger(__name__)


# Заполнение многоугольника с помощью квазислучайных точек,
# полученных из последовательности Халтона.

def halton(P: Polygon,
           margin: float,
           n_points: int,
           p1: int,
           p2: int,
           start: int = 1,
           step: int = 1) -> list[Point]:
    """
    Заполнение многоугольника с помощью квазислучайных точек, полученных из последовательности Халтона
    :param P: Многоугольник, внутри которого генерируются точки.
    :param margin: Смещение границ описанного прямоугольника.
    :param n_points: Количество точек, которое нужно сгенерировать.
    :param p1: Параметр последовательности Халтона для оси х.
    :param p2: Параметр последовательности Халтона для оси у.
    :param start: Номер первого элемента последовательности, который возьмём.
    :param step: Шаг, с которым берём элементы.
    :return: Список сгенерированных точек.
    """
    (minx, miny, maxx, maxy) = P.bounds
    P_described = Polygon(
        [Point(minx - margin, miny - margin), Point(maxx + margin, miny - margin), Point(maxx + margin, maxy + margin),
         Point(minx - margin, maxy + margin)])

    (minx, miny, maxx, maxy) = P_described.bounds
    coef_x = maxx - minx  # Коэффициенты, чтобы растянуть точки на весь многоугольник.
    coef_y = maxy - miny

    ans = []
    i = start
    while len(ans) < n_points:
        dx = get_halton(i, p1)
        dy = get_halton(i, p2)
        C = Point(minx + coef_x * dx, miny + coef_y * dy)
        if P.contains(C):
            ans.append(C)
        i += step
    logger.info('Algorithm finished successfully')
    return ans


def get_halton(n: int, base: int):
    ans = 0
    i = -1
    while n > 0:
        d = n % base
        n //= base
        ans += d * (base ** i)
        i -= 1
    return ans

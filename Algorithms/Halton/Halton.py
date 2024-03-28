from shapely import Polygon, Point
import logging

logger = logging.getLogger(__name__)


# Заполнение многоугольника с помощью квазислучайных точек,
# полученных с помощью последовательности Хэлтона.

def halton(P: Polygon,
           margin: float,
           n_points: int,
           p1: int,
           p2: int,
           start: int = 1,
           step: int = 1) -> list[Point]:
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

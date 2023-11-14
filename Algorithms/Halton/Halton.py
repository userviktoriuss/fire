from shapely import Polygon, Point


# Заполнение многоугольника с помощью квазислучайных точек,
# полученных с помощью последовательности Хэлтона.

def halton(P: Polygon,
           n_points: int,
           p1: int,
           p2: int,
           start: int = 1,
           step: int = 1) -> list[Point]:
    (minx, miny, maxx, maxy) = P.bounds
    coef_x = maxx - minx  # Коэффициенты, чтобы растянуть точки на весь многоугольник.
    coef_y = maxy - miny

    ans = []
    for i in range(start, start + n_points * step, step):
        dx = get_halton(i, p1)
        dy = get_halton(i, p2)
        C = Point(minx + coef_x * dx, miny + coef_y * dy)
        if P.contains(C):
            ans.append(C)
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

import math

EPS = 1e-16  # Эта константа показывает, какие значения считаем нулевыми.


class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other: 'Vector') -> 'Point':
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Vector') -> 'Point':
        return self + (-1 * other)

    def __str__(self) -> str:
        return f"(x={self.x}, y={self.y})"


class Vector:
    @classmethod
    def zeros(cls):
        v = Vector(Point(0, 0), Point(0, 0))
        return v

    @classmethod
    def cords(cls, x, y):
        return Vector(Point(0, 0), Point(x, y))

    def __init__(self, A: Point, B: Point):
        self.x = B.x - A.x
        self.y = B.y - A.y

    def __neg__(self):
        return Vector.cords(-self.x, -self.y)

    def __sub__(self, other: 'Vector') -> 'Vector':
        v = Vector(Point(0, 0), Point(0, 0))
        v.x = self.x - other.x
        v.y = self.y - other.y
        return v

    def __add__(self, other: 'Vector') -> 'Vector':
        v = Vector(Point(0, 0), Point(0, 0))
        v.x = self.x + other.x
        v.y = self.y + other.y
        return v

    def __rmul__(self, other: float) -> 'Vector':
        return Vector(Point(0, 0), Point(self.x * other, self.y * other))

    def __truediv__(self, other: float):
        return (1 / other) * self

    def rotate(self, alpha: float) -> 'Vector':
        """
        Поворачивает вектор на заданный угол.

        :param alpha: Угол поворота в радианах.
        :return: Копию исходного вектора, повёрнутую на угол alpha.
        """

        p_x = self.x * math.cos(alpha) - self.y * math.sin(alpha)
        p_y = self.x * math.sin(alpha) + self.y * math.cos(alpha)
        return Vector(Point(0, 0), Point(p_x, p_y))

    def length(self) -> float:
        """
        Вычисляет длину текущего вектора.
        :return: Длину вектора.
        """
        return math.sqrt(self.x ** 2 + self.y ** 2)


class Polygon:
    """
    Описывает n-угольник.
    """

    def __init__(self, vertexes: list):
        self.vertexes = vertexes
        self.n = len(vertexes)
        self.geom_center = geom_center([(p, 1) for p in vertexes])  # Взвешенный центр многоугольника.

    def point_inside(self, A: Point) -> bool:  # TODO: переписать, чтобы считалось за log
        """
        Проверяет, что точка лежит внутри многоугольника.

        :param A: Точка.
        :return: True, если точка внутри или на границе многоугольника,
        False - иначе.
        """
        angle = 0
        for i in range(self.n):
            j = (i + 1) % self.n
            v1 = Vector(A, self.vertexes[i])
            v2 = Vector(A, self.vertexes[j])
            if v1.length() <= EPS or v2.length() <= EPS:
                continue  # Считаем угол равным нулю.
            sin = cross(v1, v2) / v1.length() / v2.length()
            sin = min(1, max(-1, sin))
            alp = math.asin(sin)
            angle += alp

        return abs(angle) > math.pi

    def intersects_line(self, A: Point, AB: Vector) -> bool:
        """
        Проверяет, пересекается ли этот многоугольник с прямой,
        заданной точкой и вектором

        :param A:
        :param AB:
        :return:
        """
        for i in range(self.n):
            j = (i + 1) % self.n

            v1 = Vector(A, self.vertexes[i])
            v2 = Vector(A, self.vertexes[j])

            if vector_between_vectors(v1, AB, v2):
                return True
        return False


def dot(u: Vector, v: Vector) -> float:
    """
    Скалярное произведение двух векторов.

    :param u: Первый вектор.
    :param v: Второй вектор.
    :return: Скалярное произведение.
    """
    return u.x * v.x + u.y * v.y


def cross(u: Vector, v: Vector) -> float:
    """
    Косое произведение двух векторов.

    :param u: Первый вектор.
    :param v: Второй вектор.
    :return: Косое произведение.
    """
    return u.x * v.y - u.y * v.x


def vector_between_vectors(OA: Vector, OC: Vector, OB: Vector) -> bool:
    """
    Проверяет, что вектор лежит нестрого между
    двумя данными векторами, образующими угол.

    :param OA: Первый вектор.
    :param OC: Вектор, расположение которого проверяем.
    :param OB: Второй вектор.
    :return: True, если лежит нестрого между
    данными векторами, False - иначе.
    """

    return cross(OA, OC) * cross(OC, OB) >= 0


def intersect(A: Point, AB: Vector, C: Point, CD: Vector) -> Point:
    """
    Пересекает прямые, заданные точкой и вектором.
    Прямые не должны быть параллельны.

    :param A: Точка первой прямой.
    :param AB: Направляющий вектор первой прямой.
    :param C: Точка второй прямой.
    :param CD: Направляющий вектор второй прямой.
    :return: Точку пересечения прямых. Выбрасывает ошибку TBA,
    если прямые параллельны.
    """
    numer = (A.y - C.y) * CD.x - (A.x - C.x) * CD.y
    denom = cross(AB, CD)
    t = numer / denom
    return A + t * AB


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


def geom_center(arr: list) -> Point:
    """
    Вычисляет взвешенное среднее точек.

    :param arr: Массив пар (точка, вес)
    :return: Точка - среднее взвешенное.
    """

    sum_x = 0
    sum_y = 0
    sum_m = 0
    for (p, m) in arr:
        sum_x += p.x * m
        sum_y += p.y * m
        sum_m += m

    return Point(sum_x / sum_m, sum_y / sum_m)


def norm(v: Vector):
    return v / v.length()


class Bounding:
    """Описывает прямоугольник, в который заключена
    интересующая область плоскости."""

    def __init__(self,
                 left: float,
                 right: float,
                 up: float,
                 down: float):
        self.left = left
        self.right = right
        self.up = up
        self.down = down

    @classmethod
    def from_polygon(cls, P: Polygon):
        xs = [p.x for p in P.vertexes]
        ys = [p.y for p in P.vertexes]
        return cls(min(xs), max(xs), max(ys), min(ys))


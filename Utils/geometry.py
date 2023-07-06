import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return self + (-1 * other)

    def __str__(self):
        return f"(x={self.x}, y={self.y})"


class Vector:
    def __init__(self, A: Point, B: Point):
        self.x = B.x - A.x
        self.y = B.y - A.y

    def __rmul__(self, other):
        return Vector(Point(0, 0), Point(self.x * other, self.y * other))

    def rotate(self, alpha):
        """
        Поворачивает вектор на заданный угол.

        :param alpha: Угол поворота в радианах.
        :return: Копию исходного вектора, повёрнутую на угол alpha.
        """

        p_x = self.x * math.cos(alpha) - self.y * math.sin(alpha)
        p_y = self.x * math.sin(alpha) + self.y * math.cos(alpha)
        return Vector(Point(0, 0), Point(p_x, p_y))

    def length(self):
        """
        Вычисляет длину текущего вектора.
        :return: Длину вектора.
        """
        return math.sqrt(self.x ** 2 + self.y ** 2)


class Polygon:
    """
    Описывает n-угольник.
    """

    def __init__(self, vertexes):
        self.vertexes = vertexes
        self.n = len(vertexes)

    def point_inside(self, A):  # TODO: переписать, чтобы считалось за log
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
            sin = cross(v1, v2) / v1.length() / v2.length()
            alp = math.asin(sin)
            angle += alp

        return abs(angle) > math.pi

    def intersects_line(self, A: Point, AB: Vector):
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


def dot(u, v):
    """
    Скалярное произведение двух векторов.

    :param u: Первый вектор.
    :param v: Второй вектор.
    :return: Скалярное произведение.
    """
    return u.x * v.x + u.y * v.y


def cross(u, v):
    """
    Косое произведение двух векторов.

    :param u: Первый вектор.
    :param v: Второй вектор.
    :return: Косое произведение.
    """
    return u.x * v.y - u.y * v.x


def vector_between_vectors(OA, OC, OB):
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


def intersect(A: Point, AB: Vector, C: Point, CD: Vector):
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


def sign(a):
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
    elif a < 0:
        return 1
    return -1

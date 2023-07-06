from Utils.geometry import *

# Заполнение путём построения шестиугольной сетки.
# Строит сетку и возвращает центры шестиугольников,
# которые попали внутрь заданного многоугольника

def hexagonal(P, sx=0, sy=0, a=1, alpha=0):
    """
    Строит шестиугольную сетку с начальной точкой O=(sx, sy), длиной
    стороны шестиугольника равной a и повёрнутой на угол alpha
    относительно O внутри многоугольника P. Возвращает список точек - центры
    шестиугольников, которые попали внутрь многоугольника P.

    :param P: Многоугольник.
    :param sx: Координата x стартовой точки.
    :param sy: Координата y стартовой точки.
    :param a: Длина стороны шестиугольников сетки.
    :param alpha: Угол поворота сетки [0; pi/6]
    :return: Центры соответствующих шестиугольников.
    """
    # TODO: вроде как я сейчас поворачиваю относительно нуля, а надо бы
    #  относительно S

    S = Point(sx, sy)
    i = Vector(S, Point(sx + a * math.sqrt(3), sy)).rotate(alpha)
    # расстояние между параллельными прямыми равно sqrt(3)/2 a
    ort_i = Vector(S, Point(sx, sy + math.sqrt(3) * a / 2)).rotate(alpha)
    j = i.rotate(math.pi / 3)
    ort_j = ort_i.rotate(math.pi / 3)

    # TODO: оператор - для точки и вектора
    horizontal = get_parallel(S, i, ort_i, P)  # все линии, параллельные i
    oblique = get_parallel(S, j, ort_j, P)  # все линии, параллельные j

    inside = []
    for hor in horizontal:
        for obl in oblique:
            C = intersect(hor, i, obl, j)
            if P.point_inside(C):
                inside.append(C)
    return inside

def get_parallel(S, i, ort_i, P):
    # пересечь с каждой стороной и проверить, что хотя бы одно
    # пересечение лежит на границе многоугольника.
    iteration = 0
    parallel = []

    while True:
        cur_up = S + iteration * ort_i
        cur_down = S - iteration * ort_i

        added_any = False
        if P.intersects_line(cur_up, i):
            parallel.append(cur_up)
            added_any = True

        if P.intersects_line(cur_down, i):
            parallel.append(cur_down)
            added_any = True

        if not added_any:
            break
        iteration += 1

    return parallel



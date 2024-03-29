import numpy as np
from shapely import Point, Polygon

from Algorithms.NBodies.GravityFunctions.GravityFunctions import cut_gravity_with_base_direction, \
    repel_cut_gravity_with_base_direction


# В этом файле заданы различные функции гравитации между кругом и многоугольником.


def side_gravity(A: Point, P: Polygon, G_in: float, G_out: float, STOP_RADIUS: float) -> np.array:
    """
    Если точка внутри многоугольника, вернёт {0; 0}.
    Иначе найдёт проекцию точки на многоугольник и посчитает
    для неё и A cut_gravity() с заданными параметрами.

    :param A: Точка.
    :param P: Многоугольник.
    :param G_in: Гравитационная постоянная, когда точка внутри P.
    :param G_out: Гравитационная постоянная, когда точка вне P.
    :param STOP_RADIUS: Критический радиус для перехода с Ньютоновской
    гравитации на отрезок параболы.
    :return: Вектор np.array, хранящий координаты вектора силы.
    """

    dist = P.exterior.project(A)
    proj = P.exterior.interpolate(dist)  # Точка - проекция А на P.

    if P.contains(A):
        # Внутри многоугольника стенки всё равно толкают круг
        return repel_cut_gravity_with_base_direction(
            np.array(A.xy).flatten(),
            np.array(proj.xy).flatten(),
            G_in,
            STOP_RADIUS * 0.1)  # TODO: убрать коэф

    return cut_gravity_with_base_direction(
        np.array(A.xy).flatten(),
        np.array(proj.xy).flatten(),
        G_out,
        STOP_RADIUS,
        np.array(P.centroid.xy).flatten())

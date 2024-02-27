import numpy as np

"""
В этом файле заданы различные функции гравитации.
Описание этих функций ищите в GravityFunctions.md
"""


def gravity(A, B, G=6.67430):
    """
    Перемещение тела А в сторону тела B по закону гравитации.

    :param A: Пара координат тела А.
    :param B: Пара координат тела В.
    :return: Величина перемещения в сторону тела В.
    """
    return G * 1 * 1 * (B - A) / np.linalg.norm(B - A) ** 3


def cut_gravity(A, B, G=6.67430, STOP_RADIUS=1.5):
    """
    Перемещение тела А в сторону тела B по закону гравитации.
    Если расстояние между телами меньше STOP_RADIUS, то
    перемещение будет как будто расстояние было равно STOP_RADIUS

    :param A: Пара координат тела А.
    :param B: Пара координат тела В.
    :return: Величина перемещения в сторону тела В.
    """
    ln = np.linalg.norm(B - A)
    rho = max(ln, STOP_RADIUS)
    dir = (B - A) / rho
    module = G * 1 * 1 / rho ** 2
    return module * dir


def gravity_with_sign(A, B, G=6.67430, STOP_RADIUS=1.5):
    ln = np.linalg.norm(B - A)
    rho = ln - STOP_RADIUS
    return gravity(A, B, G) * np.sign(rho)


def cut_gravity_with_sign(A, B, G=6.67430, STOP_RADIUS=1):  # 1.5
    ln = np.linalg.norm(B - A)
    rho = ln - STOP_RADIUS
    return cut_gravity(A, B, G, STOP_RADIUS) * np.sign(rho)


def zeroed_gravity(A, B, G=6.67430, STOP_RADIUS=1.5):
    # Если ближе STOP_RADIUS, то просто 0
    ln = np.linalg.norm(B - A)
    dir = (B - A) / ln
    if ln < STOP_RADIUS:
        module = 0
    else:
        module = G * 1 * 1 / ln ** 2
    return module * dir


def smooth_gravity_with_sign(A, B, G=6.67430, STOP_RADIUS=1.5):
    ln = np.linalg.norm(B - A)
    if ln >= STOP_RADIUS:
        return gravity(A, B, G)

    s = STOP_RADIUS
    x = G * 1 * 1 / s ** 2

    # Коэффициенты параболы
    a = x / s / (s + 2 * x)
    b = 2 * a * x
    c = -2 * x

    if ln < 1e-14:
        dir = np.array([0, 0]).astype('float')
    else:
        dir = (B - A) / ln
    module = a * ln ** 2 + b * ln + c
    return module * dir


def smooth_gravity_on_region_with_sign(A, B, G=6.67430, STOP_RADIUS=1.5, REGION_RADIUS=2.5):
    ln = np.linalg.norm(B - A)
    if ln > REGION_RADIUS:
        return np.zeros(2)
    return smooth_gravity_with_sign(A, B, G, STOP_RADIUS)


def repel_cut_gravity(A, B, G=6.67430, STOP_RADIUS=1.5):
    """
    То же, что и cut_gravity, но работает на отталкивание
    :param A: Первая точка.
    :param B: Вторая точка.
    :param G: Гравитационная постоянная.
    :param STOP_RADIUS: Радиус отсечения бесконечного хвоста
    :return: Величина перемещения в сторону тела B.
    """
    return cut_gravity(
        B,
        A,
        G,
        STOP_RADIUS)

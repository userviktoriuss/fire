import math
import random

import numpy as np
from shapely.ops import unary_union

from Algorithms.Genetic.Population import Being
from Utils.Circle import Circle, Point
from shapely import Polygon

"""
Устройство метода:
1) Найдём плохие круги
2) Для каждого плохого круга создадим ветку: без него, или с ним,но сдвинутым под некоторым углом на случайное растояние
3) Оценим каждую ветку и выберем более перспективную из всех
Среди всех особей также будем поддерживать самую лучшую.

Плохие круги бывают двух типов:
1) имеющие наибольшее пересечение с другими кругами
2) имеющие наименьшее пересечение с многоугольником

Оценка веток на перспективность:

Выбор лучшей особи:
"""


def bnb(P: Polygon,
        centers: list[Point],
        radius: float = 1,
        max_iterations: int = 100,
        is_repaired: bool = False,
        ALPHA: float = 2.1,
        BETA: float = 0.8,
        GAMMA: float = 0.5,
        ANGLE_RESOLUTION: int=6,
        MOVE_MULTIPLIER: float=1.5):
    circles = [Circle(p, radius) for p in centers]
    b = Being(P, radius, circles)
    best = b
    init_circles = len(centers)

    while max_iterations > 0 and not b.covers_polygon:
        bad_inds = find_bad_circles(b)  # Найдём плохие круги.
        branches = create_branches(b, bad_inds, ANGLE_RESOLUTION, MOVE_MULTIPLIER)  # Построим ветви
        fitness(branches, ALPHA, BETA, GAMMA, init_circles)  # Оценить перспективность ветвей
        cur_best = np.argmax([being.fitness for being in branches])  # Выбрать лучшую из встретившихся ветвей
        b = branches[cur_best]  # Выбрать ветвь.

        if best.fitness < branches[cur_best].fitness:
            best = branches[cur_best]  # Сохранить лучшую из всех особей.

    if is_repaired:
        # TODO: запустить BFGS или barons с маоенькими значениями, чтобы увеличить площадь покрытия
        pass  # чиним best
    return [p.center for p in best.circles]


def fitness(beings: list[Being],
            ALPHA: float,
            BETA: float,
            GAMMA: float,
            init_circles):
    for being in beings:
        outside = 0
        self_inter = 0
        for circle in being.circles:
            outside += circle.area - being.polygon.intersection(circle.polygon).area
            without = [c.polygon for c in being.circles if c != circle]
            self_inter += unary_union(without).intersection(circle.polygon).area / circle.area

        outside /= being.polygon.area
        self_inter /= unary_union([c.polygon for c in being.circles]).area
        circle_count = len(being.circles) / init_circles
        being.fitness = (ALPHA * (1 - self_inter) +
                         BETA * (1 - outside) +
                         GAMMA * (1 - circle_count))


# Находит плохие круги
# Плохие круги:
#   1) Имеющий наибольшее пересечение с другими кругами,
#   2) Имеющий наименьшее пересечение с многоугольником.
def find_bad_circles(b: Being) -> list[int]:
    min_inter = float('inf')  # Минимальное пересечение с многоугольником.
    min_inter_ind = 0  # Соответствующий круг.

    max_self = -1  # Максимальное пересечение с другими кругами.
    max_self_ind = 0  # Соответствующий круг.

    for i in range(len(b.circles)):
        cur_inter = b.polygon.intersection(b.circles[i].polygon).area
        if cur_inter < min_inter:
            min_inter = cur_inter
            min_inter_ind = i

        near = [c.polygon
                for c in b.circles
                if c != b.circles[i] and c.distance(b.circles[i]) < 2 * b.circles[i].radius]
        cur_self = unary_union(near).intersection(b.circles[i]).area

        if cur_self > max_self:
            max_self = cur_self
            max_self_ind = i
    return [min_inter_ind, max_self_ind]

# Создаёт несколько возможных ветвей для существа
def create_branches(b: Being,
                    bad_inds: list[int],
                    ANGLE_RESOLUTION: int,
                    MOVE_MULTIPLIER: float) -> list[Being]:
    branches = []
    for bad_ind in bad_inds:
        without = [b.circles[i] for i in range(len(b.circles)) if i != bad_ind]
        bad = b.circles[bad_ind]
        # Удалим круг
        branches.append(Being.from_circles(b.polygon, without))

        # Подвигаем круг
        for i in range(ANGLE_RESOLUTION):
            angle = 360 * i / ANGLE_RESOLUTION
            dist = random.uniform(0, MOVE_MULTIPLIER * b.circles[0].radius)  # TODO: или другое распределение
            dx = dist * math.cos(angle)
            dy = dist * math.sin(angle)
            new_circle = Circle(Point(bad.center.x + dx, bad.center.y + dy),
                                bad.radius)
            branches.append(Being.from_circles(b.polygon,
                                               without + [new_circle]))
    return branches

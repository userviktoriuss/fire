import math
import random

import numpy as np
from shapely.ops import unary_union

from Algorithms.Baron.BaronsAlgorithm import BaronsAlgorithm
from Algorithms.Genetic.Population import Being, Population
from Utils.Circle import Circle, Point
from shapely import Polygon

# TODO: оформить устройство, чтобы потом в доку было проще писать
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
        max_iterations: int = 60, # 2.5 n работает неплохо
        is_repaired: bool = False,
        ALPHA: float = -0.3,  # Влияние самопересечений.
        BETA: float = 0.3,  # Влияние отношения покрытой площади вне многоугольника к площади многоугольника.
        GAMMA: float = 0.005,  # Влияние количества кругов по отношению к стартовому.
        LAMBDA: float = 1.0,  # Влияние процента покрытия.
        ANGLE_RESOLUTION: int=6,
        MOVE_MULTIPLIER: float=1.5,
        DELETE_PROB: float=0.05):
    circles = [Circle(p, radius) for p in centers]
    b = Being(P, radius, circles)
    best = b
    init_circles = len(centers)

    fitness([best], ALPHA, BETA, GAMMA, LAMBDA, init_circles)

    while max_iterations > 0 and not b.covers_polygon and len(b.circles) > 0:
        bad_inds = find_bad_circles(b)  # Найдём плохие круги.
        branches = create_branches(b, bad_inds, ANGLE_RESOLUTION, MOVE_MULTIPLIER, DELETE_PROB)  # Построим ветви
        fitness(branches, ALPHA, BETA, GAMMA, LAMBDA, init_circles)  # Оценить перспективность ветвей
        cur_best = np.argmax([being.fitness for being in branches])  # Выбрать лучшую из встретившихся ветвей
        b = branches[cur_best]  # Выбрать ветвь.

        if best.fitness < branches[cur_best].fitness:
            best = branches[cur_best]  # Сохранить лучшую из всех особей.
        print(best.fitness)
        max_iterations -= 1

    if is_repaired:
        alg = BaronsAlgorithm(
            polygon=P,
            n_barons=len(b.circles),
            radius=radius,
            init_circles=b.circles
        )

        alg.run_algorithm(
            init_tau=1e-3,
            end_tau=1e-5,
            change_tau=0.995,
            regular_mult=1,
            half_mult=1.3,
            far_mult=1.7,
            covered_mult=1,
            verbose=True
        )

        best = alg.get_circles()
        return [p.center for p in best]
    return [p.center for p in best.circles]


def fitness(beings: list[Being],
            ALPHA: float,
            BETA: float,
            GAMMA: float,
            LAMBDA: float,
            init_circles):
    for being in beings:
        outside = 0
        self_inter = 0
        for circle in being.circles:
            outside += circle.area - being.polygon.intersection(circle.polygon).area
            without = [c.polygon for c in being.circles if c != circle]
            self_inter += unary_union(without).intersection(circle.polygon).area / circle.area

        outside /= being.polygon.area
        all_union = unary_union([c.polygon for c in being.circles])
        self_inter /= all_union.area
        circle_count = len(being.circles) / init_circles

        coverage = all_union.intersection(being.polygon).area / being.polygon.area

        being.fitness = (ALPHA * (1 - self_inter) +
                         BETA * (1 - outside) +
                         GAMMA * (1 - circle_count) +
                         LAMBDA * coverage)


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

        near = [c.polygon  # TODO: создать сетку, чтобы не делать такой сложный цикл
                for c in b.circles
                if c != b.circles[i] and c.center.distance(b.circles[i].center) < 2 * b.circles[i].radius]
        cur_self = unary_union(near).intersection(b.circles[i].polygon).area

        if cur_self > max_self:
            max_self = cur_self
            max_self_ind = i
    return [min_inter_ind, max_self_ind]

# Создаёт несколько возможных ветвей для существа
def create_branches(b: Being,
                    bad_inds: list[int],
                    ANGLE_RESOLUTION: int,
                    MOVE_MULTIPLIER: float,
                    DELETE_PROB: float) -> list[Being]:
    branches = []
    for bad_ind in bad_inds:
        without = [b.circles[i] for i in range(len(b.circles)) if i != bad_ind]
        bad = b.circles[bad_ind]

        # Удалим круг
        if random.random() < DELETE_PROB:
            branches.append(Being.from_circles(b.polygon, without))

        # Подвигаем круг
        for i in range(ANGLE_RESOLUTION):
            angle = 360 * i / ANGLE_RESOLUTION
            sigma = MOVE_MULTIPLIER * b.circles[0].radius / 3 #  По правилу трёх сигм получаем среднеквадратическое отклонение.
            dist = random.uniform(0, sigma * sigma)
            dx = dist * math.cos(angle)
            dy = dist * math.sin(angle)
            new_circle = Circle(Point(bad.center.x + dx, bad.center.y + dy),
                                bad.radius)
            branches.append(Being.from_circles(b.polygon,
                                               without + [new_circle]))
    return branches

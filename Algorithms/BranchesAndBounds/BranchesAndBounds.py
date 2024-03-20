import math
import random
import time

import numpy as np
from shapely.ops import unary_union

from Algorithms.Algorithm import Algorithm
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


class BnBAlgorithm(Algorithm):
    def __init__(self,
                 P: Polygon,
                 circles: list[Circle],
                 radius: float = 1):
        self.P = P
        self.circles = circles
        self.radius = radius

    def set_params(self,
                   max_iterations: int = 60,  # 2.5 n работает неплохо
                   is_repaired: bool = False,
                   ALPHA: float = -0.3,  # Влияние самопересечений.
                   BETA: float = 0.3,  # Влияние отношения покрытой площади вне многоугольника к площади многоугольника.
                   GAMMA: float = 0.005,  # Влияние количества кругов по отношению к стартовому.
                   LAMBDA: float = 1.0,  # Влияние процента покрытия.
                   ANGLE_RESOLUTION: int = 6,
                   MOVE_MULTIPLIER: float = 1.5,
                   MOVE_SCHEDULE=(lambda x: x),
                   DELETE_PROB: float = 0.05,
                   fixed: list[int] = None
                   ):
        self.max_iterations = max_iterations
        self.is_repaired = is_repaired
        self.ALPHA = ALPHA
        self.BETA = BETA
        self.GAMMA = GAMMA
        self.LAMBDA = LAMBDA
        self.ANGLE_RESOLUTION = ANGLE_RESOLUTION
        self.MOVE_MULTIPLIER = MOVE_MULTIPLIER
        self.MOVE_SCHEDULE = MOVE_SCHEDULE
        self.DELETE_PROB = DELETE_PROB
        if fixed is None:
            self.fixed = [0] * len(self.circles)
        else:
            self.fixed = fixed

    def run_algorithm(self):
        b = Being(self.P, self.radius, self.circles)

        best = b
        self.init_circles = len(self.circles)

        self.__fitness([best])
        iterations_left = self.max_iterations
        self.CUR_MOVE_MULTIPLIER = self.MOVE_MULTIPLIER
        # TODO: запретить действия согласно fixed
        while iterations_left > 0 and not b.covers_polygon and len(b.circles) > 0:
            bad_inds = self.__find_bad_circles(b)  # Найдём плохие круги.
            branches = self.__create_branches(b, bad_inds)  # Построим ветви
            self.__fitness([b[0] for b in branches])  # Оценить перспективность ветвей
            cur_best = np.argmax(
                [being.fitness for (being, action, ind) in branches])  # Выбрать лучшую из встретившихся ветвей
            b = branches[cur_best][0]  # Выбрать ветвь.
            if branches[cur_best][1] == 'delete':  # Если выбрали ветвь с удалением, нужно поправить массив неподвижных кругов.
                del self.fixed[branches[cur_best][2]]
            else: # Если выбрали ветвь с передвижением, сдвинутый круг стал последним (особенность реализации)
                save = self.fixed[branches[cur_best][2]]
                del self.fixed[branches[cur_best][2]]
                self.fixed.append(save)

            if best.fitness < b.fitness:
                best = b  # Сохранить лучшую из всех особей.

            self.CUR_MOVE_MULTIPLIER = self.MOVE_SCHEDULE(self.CUR_MOVE_MULTIPLIER)
            iterations_left -= 1

        if self.is_repaired:
            t0 = time.perf_counter()
            alg = BaronsAlgorithm(
                polygon=self.P,
                n_barons=len(b.circles),
                radius=self.radius,
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
                verbose=False
            )
            t1 = time.perf_counter()
            print(f'Repair ended in {t1 - t0} sec.')
            self.circles = alg.get_circles()
            return
        self.circles = best.circles

    def get_result(self) -> list[Circle]:
        return self.circles

    def __fitness(self, beings: list[Being]):
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
            circle_count = len(being.circles) / self.init_circles

            coverage = all_union.intersection(being.polygon).area / being.polygon.area

            being.fitness = (self.ALPHA * (1 - self_inter) +
                             self.BETA * (1 - outside) +
                             self.GAMMA * (1 - circle_count) +
                             self.LAMBDA * coverage)

    # Находит плохие круги
    # Плохие круги:
    #   1) Имеющий наибольшее пересечение с другими кругами,
    #   2) Имеющий наименьшее пересечение с многоугольником.
    def __find_bad_circles(self, b: Being) -> list[int]:
        min_inter = float('inf')  # Минимальное пересечение с многоугольником.
        min_inter_ind = -1  # Соответствующий круг.

        max_self = -1  # Максимальное пересечение с другими кругами.
        max_self_ind = -1  # Соответствующий круг.

        for i in range(len(b.circles)):
            if self.fixed[i]:
                continue
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

        ans = []
        if min_inter_ind != -1:
            ans.append(min_inter_ind)
        if max_self_ind != -1:
            ans.append(max_self_ind)
        return ans

    # Создаёт несколько возможных ветвей для существа
    def __create_branches(self,
                          b: Being,
                          bad_inds: list[int]) -> list[(Being, str, int)]:
        branches = []
        for bad_ind in bad_inds:
            without = [b.circles[i] for i in range(len(b.circles)) if i != bad_ind]
            bad = b.circles[bad_ind]

            # Удалим круг
            if random.random() < self.DELETE_PROB:
                branches.append((Being.from_circles(b.polygon, without), 'delete', bad_ind))

            # Подвигаем круг
            for i in range(self.ANGLE_RESOLUTION):
                angle = 360 * i / self.ANGLE_RESOLUTION
                sigma = self.CUR_MOVE_MULTIPLIER * b.circles[
                    0].radius / 3  # По правилу трёх сигм получаем среднеквадратическое отклонение.
                dist = np.random.normal(0, sigma * sigma)
                dx = dist * math.cos(angle)
                dy = dist * math.sin(angle)
                new_circle = Circle(Point(bad.center.x + dx, bad.center.y + dy),
                                    bad.radius)
                branches.append((Being.from_circles(b.polygon,
                                                    without + [new_circle]), 'move', bad_ind))
        return branches

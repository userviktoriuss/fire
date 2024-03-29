import math

import numpy as np
from shapely import Polygon, unary_union, Point

from Algorithms.BranchesAndBounds.Loggers.BnBAnimationLogger import BnBAnimationLogger
from Algorithms.BranchesAndBounds.Branch import Branch
from Algorithms.BranchesAndBounds.Loggers.BnBMetricLogger import BnBMetricLogger
from Utils.Circle import Circle


class FlexibleBnBParams:
    """
    Набор функций, параметризующих работу метода ветвей и границ.
    Алгоритм использует интерфейс этого класса, так что для создания
    своих реализаций стоит наследоваться от этого класса.
    """

    def __init__(self,
                 P: Polygon,
                 init_circles: int,
                 SELF_INTER_W: float = 0,
                 OUTSIDE_W: float = 0.05,
                 CIRCLE_COUNT_W: float = 0.005,
                 COVERAGE_W: float = 1.5,
                 ANGLE_RESOLUTION: int = 6,
                 MOVE_MULTIPLIER: float = 1.5,
                 MOVE_SCHEDULE=(lambda x: x),
                 animation_logger: BnBAnimationLogger = None,
                 metric_logger: BnBMetricLogger = None):
        self.P = P
        self.init_circles = init_circles

        self.SELF_INTER_W = SELF_INTER_W
        self.OUTSIDE_W = OUTSIDE_W
        self.CIRCLE_COUNT_W = CIRCLE_COUNT_W
        self.COVERAGE_W = COVERAGE_W

        self.ANGLE_RESOLUTION = ANGLE_RESOLUTION

        self.MOVE_MULTIPLIER = MOVE_MULTIPLIER
        self.MOVE_SCHEDULE = MOVE_SCHEDULE

        self.animation_logger = animation_logger
        self.metric_logger = metric_logger

        # Приготовим для работы логгеры.
        if self.animation_logger:
            (minx, miny, maxx, maxy) = self.P.bounds
            self.animation_logger.reset((minx - 1, maxx + 1), (miny - 1, maxy + 1))

        if self.metric_logger:
            self.metric_logger.reset(['1 - self_inter', '1 - outside', '1 - circle_count', 'coverage'])


    def reset(self):
        """
        Готовит параметры для новой итерации алгоритма.
        """
        self.cur_multplier = self.MOVE_MULTIPLIER

    def find_bad_circles(self, branch: Branch) -> list[int]:
        """
        Находит индексы 'плохих' кругов для данной ветви.

        :param branch: Ветвь.
        :return: Массив индексов.
        """

        # Плохие круги:
        #   1) Имеющий наибольшее пересечение с другими кругами,
        #   2) Имеющий наименьшее пересечение с многоугольником.

        min_inter = float('inf')  # Минимальное пересечение с многоугольником.
        min_inter_ind = -1  # Соответствующий круг.

        max_self = -1  # Максимальное пересечение с другими кругами.
        max_self_ind = -1  # Соответствующий круг.

        for i in range(len(branch.circles)):
            if branch.fixed[i]:
                continue
            cur_inter = branch.polygon.intersection(branch.circles[i].polygon).area
            if cur_inter < min_inter:
                min_inter = cur_inter
                min_inter_ind = i

            # Круги, которые недалеко от i-го.
            near = [c.polygon  # TODO: создать сетку, чтобы не делать такой сложный цикл
                    for c in branch.circles
                    if c != branch.circles[i] and
                    c.center.distance(branch.circles[i].center) < 2 * branch.circles[i].radius]
            cur_self = unary_union(near).intersection(branch.circles[i].polygon).area

            if cur_self > max_self:
                max_self = cur_self
                max_self_ind = i

        ans = []
        if min_inter_ind != -1:
            ans.append(min_inter_ind)
        if max_self_ind != -1:
            ans.append(max_self_ind)
        return ans

    def create_branches(self,
                        b: Branch,
                        bad_inds: list[int]) -> list[Branch]:
        """
        По заданному набору индексов 'плохих' кругов строит ветви, которые
        попробуют решить их проблемы.

        :param b: Ветвь, из которой создаём новые.
        :param bad_inds: Индексы 'плохих' кругов.
        :return: Массив ветвей.
        """
        branches = []
        for bad_ind in bad_inds:
            without = [b.circles[i] for i in range(len(b.circles)) if i != bad_ind]
            bad = b.circles[bad_ind]  # Сам плохой круг.

            # Удалим круг
            new_fixed = b.fixed[:bad_ind] + b.fixed[bad_ind + 1:]
            branches.append(Branch(b.polygon, without, new_fixed))

            # Подвигаем круг
            for i in range(self.ANGLE_RESOLUTION):
                angle = 360 * i / self.ANGLE_RESOLUTION  # Подвинем в каждом из ANGLE_RESOLUTION направлений.
                sigma = self.cur_multplier * b.circles[
                    0].radius / 3  # По правилу трёх сигм получаем среднеквадратическое отклонение так, чтобы кружок
                # почти всегда двигался не больше чем на радиус.

                dist = np.random.normal(0, sigma * sigma)  # Расстояние, на которое сдвинем кружок.
                dx = dist * math.cos(angle)  # Проекция на оси координат.
                dy = dist * math.sin(angle)
                new_circle = Circle(Point(bad.center.x + dx, bad.center.y + dy),
                                    bad.radius)
                new_fixed = b.fixed[:bad_ind] + b.fixed[bad_ind + 1:] + [b.fixed[bad_ind]]
                branches.append(Branch(b.polygon, without + [new_circle], new_fixed))

        self.cur_multplier = self.MOVE_SCHEDULE(self.cur_multplier)
        return branches

    def calculate_metric(self, branches: list[Branch]):
        """
        Считает метрику для всех ветвей из массива branches.

        :param branches: Массив ветвей.
        """

        for branch in branches:
            outside = 0  # Площадь внешнего покрытия.
            self_inter = 0  # Суммарная площадь самопересечений кругов.
            for circle in branch.circles:
                outside += circle.area - branch.polygon.intersection(circle.polygon).area
                without = [c.polygon
                           for c in branch.circles
                           if c != circle and
                           c.center.distance(
                               circle.center) < 2 * circle.radius]
                self_inter += unary_union(without).intersection(circle.polygon).area / circle.area

            outside /= branch.polygon.area
            all_union = unary_union([c.polygon for c in branch.circles])
            self_inter /= all_union.area
            circle_count = len(branch.circles) / self.init_circles

            coverage = all_union.intersection(branch.polygon).area / branch.polygon.area

            branch.metric = (self.SELF_INTER_W * (1 - self_inter) +
                             self.OUTSIDE_W * (1 - outside) +
                             self.CIRCLE_COUNT_W * (1 - circle_count) +
                             self.COVERAGE_W * coverage)

            if self.metric_logger:
                self.metric_logger.add_info(
                    branch.metric,
                    (1 - self_inter, 1 - outside, 1 - circle_count, coverage))
        if self.metric_logger:
            self.metric_logger.harden()

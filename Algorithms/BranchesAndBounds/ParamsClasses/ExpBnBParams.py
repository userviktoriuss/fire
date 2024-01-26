import numpy as np
from shapely import unary_union

from Algorithms.BranchesAndBounds.Branch import Branch
from Algorithms.BranchesAndBounds.ParamsClasses.TripleBnBParams import TripleBnBParams


class ExpBnBParams(TripleBnBParams):
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
                               circle.center) < 2 * circle.radius]  # TODO: проверить, что работает корректно
                self_inter += unary_union(without).intersection(circle.polygon).area / circle.area

            outside /= branch.polygon.area
            all_union = unary_union([c.polygon for c in branch.circles])
            self_inter /= all_union.area
            circle_count = len(branch.circles) / self.init_circles

            coverage = all_union.intersection(branch.polygon).area / branch.polygon.area

            # Растянем coverage
            coverage = (max(coverage, 0.97) - 0.97) / 0.03

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
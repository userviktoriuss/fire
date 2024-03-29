from shapely import unary_union

from Algorithms.BranchesAndBounds.Branch import Branch
from Algorithms.BranchesAndBounds.ParamsClasses.SmarterBadCirclesBnBParams import SmarterBadCirclesBnBParams


class StretchedBnBParams(SmarterBadCirclesBnBParams):
    """
    То же, что и SmarterBadCirclesBnBParams, но равномерно растягивает метрику
    coverage из отрезка [0.96; 1] до [0; 1]
    """
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
            if all_union.area < 1e-8:
                self_inter = 0  # Очень странный случай, но появляется, когда все круги удалены.
            else:
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
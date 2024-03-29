from shapely import unary_union
from Algorithms.RedundantRemovers.RedundantRemover import RedundantRemover
import logging

logger = logging.getLogger(__name__)


class GreedyRedundantRemover(RedundantRemover):
    """
    Жадным образом удаляет круги: останутся только те, что вносят значительный по площади вклад в покрытие.
    """
    EPS = 1e-3

    def set_params(self, EPS: float = None):
        if EPS is not None:
            self.EPS = EPS

    def run_algorithm(self):
        # Оставим только те круги, которые вносят значительный вклад в покрытие.
        inside = [c for c in self.input_ if self.P.contains(c.center)]
        outside = [c for c in self.input_ if not self.P.contains(c.center)]
        union = unary_union([c.polygon for c in inside])

        outside.sort(key=
                     lambda c: self.P.intersection(c.polygon).area,
                     reverse=True)
        for c in outside:
            c_inside_polygon = self.P.intersection(c.polygon)
            united = unary_union([union, c_inside_polygon])
            if abs(united.area - union.area) > self.EPS:
                inside.append(c)
                union = unary_union([union, c_inside_polygon])

        self.circles = inside

        logger.info('Algorithm finished successfully')

import time

from Utils.Circle import *
from Algorithms.Baron.Market import Market


class BaronsAlgorithm:
    def __init__(self,
                 polygon: Polygon,
                 n_barons: int,
                 radius: float,
                 init_circles: list[Circle]=None):
        """
        Создаёт рынок баронов.
        :param polygon: Многоугольник, на котором ищем.
        :param n_barons: Стартовое количество баронов.
        :param radius: Радиус круга, соответствующего барону.
        """
        self.radius = radius
        self.market = Market(polygon, grid_size=2 * radius)
        self.market.fill_barons(n_barons, radius, init_circles)

    def run_algorithm(self,
                      init_tau: float = 0.5,
                      end_tau: float = 1e-8,
                      change_tau: float = 0.99,
                      regular_mult: float = 1,
                      half_mult: float = 1.3,
                      far_mult: float = 1.7,
                      covered_mult: float = 1,
                      verbose: bool = False) -> None:
        """
        Запускает алгоритм.
        
        :param init_tau: Стартовое значение скорости обучения.
        :param end_tau: Конечное значение скорости обучения.
        :param change_tau: Изменение скорости обучения.
        :param regular_mult: Дополнительный множитель для движения круга, имеющего пересечения с другими и находящегося в многоугольнике.
        :param half_mult: Дополнительный множитель для движения круга, имеющего пересечения с другими и находящегося снаружи многоугольнике.
        :param far_mult: Дополнительный множитель для движения круга, имеющего пересечения с другими и находящегося в многоугольнике.
        :param covered_mult: Дополнительный множитель для движения круга, полностью покрытого другими кругами.
        """
        if verbose:
            print("Initiating algorithm")
            t0 = time.perf_counter()
        tau = init_tau
        while tau > end_tau:
            self.market.next_iteration(tau, regular_mult, half_mult, far_mult, covered_mult)
            tau *= change_tau
            # TODO: progress bar

        if verbose:
            elapsed = time.perf_counter() - t0
            print(f'Algorithm ended in {elapsed} sec.')

    def get_circles(self):
        return [Circle(Point(baron.center.x, baron.center.y), self.radius)
                for cords in self.market.grid
                for baron in self.market.grid[cords]]

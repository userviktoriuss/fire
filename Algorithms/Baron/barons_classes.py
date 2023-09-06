from Utils.Circle import *


class BaronsAlgorithm:
    def __init__(self,
                 polygon: Polygon,
                 n_barons: int,
                 radius: float):
        """
        Создаёт рынок баронов.
        :param polygon: Многоугольник, на котором ищем.
        :param n_barons: Стартовое количество баронов.
        :param radius: Радиус круга, соответствующего барону.
        """
        self.barons = Market(polygon, grid_size=2 * radius)
        self.barons.fill_barons(n_barons, radius)

    def run_algorithm(self, 
                      init_tau: float = 0.5,
                 end_tau: float = 1e-8,
                 change_tau: float = 0.99,):
        """
        Запускает алгоритм.
        
        :param init_tau: Стартовое значение скорости обучения.
        :param end_tau: Конечное значение скорости обучения.
        :param change_tau: Изменение скорости обучения.
        :return: 
        """
        tau = init_tau
        while tau > end_tau:
            self.market.next_iteration(tau)
            tau *= change_tau

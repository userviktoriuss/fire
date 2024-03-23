import numpy as np

from Algorithms.BranchesAndBounds.FlexibleBnBAlgorithm import FlexibleBnBAlgorithm
from Algorithms.BranchesAndBounds.ParamsClasses.StretchedBnBParams import StretchedBnBParams
from Algorithms.RedundantRemovers.RedundantRemover import RedundantRemover
from Utils.layering import get_layers


class GeneticRedundantRemover(RedundantRemover):
    # В алгоритме круги делятся на слои по расстоянию до внешней
    # области многоугольника. Этот параметр показывает,
    # с какого слоя круги считать "внутренними".
    INNER_BOUND = 2
    def run_algorithm(self):
        # Разложим круги по уровням дальности до края многоугольника
        layers = get_layers(self.P, self.input_)

        # Выделим "внутренние" круги.
        inners = np.zeros(len(layers))
        inners[layers >= self.INNER_BOUND] = 1

        # Починим методом ветвей и границ
        bnb_alg = FlexibleBnBAlgorithm(self.P, self.input_)
        # Запустим алгоритм с приоритетом на удаление кругов.
        bnb_alg.set_params(
            max_iterations=len(self.input_),
            params=StretchedBnBParams(
                self.P,
                len(self.input_),
                CIRCLE_COUNT_W=0.1,
                MOVE_SCHEDULE=(lambda x: 0.985 * x)),
            fixed=list(inners)
        )
        bnb_alg.run_algorithm()
        self.circles = bnb_alg.get_result()

from Algorithms.Genetic.Population import *
from Utils.Circle import *
import time


class GeneticAlgorithm:  # TODO: изменить порядок классов, чтобы правильно указывать типы без кавычек
    """
    Моделирует естественный отбор.
    """

    def __init__(self,
                 polygon: Polygon,
                 init_circles: int,
                 n_beings: int = 10,
                 radius: float = 1.0,
                 SURVIVE_RATE: float = 0.8,
                 REMOVE_RATE: float = 0.1,
                 MOVE_RATE: float = 0.2,
                 ALPHA: float = 2.1,
                 BETA: float = 0.8,
                 GAMMA: float = 0.5,
                 verbose: bool = False):
        self.SURVIVE_RATE = SURVIVE_RATE
        self.REMOVE_RATE = REMOVE_RATE
        self.MOVE_RATE = MOVE_RATE
        self.ALPHA = ALPHA
        self.BETA = BETA
        self.GAMMA = GAMMA

        self.population = Population(polygon, init_circles)
        self.population.fill_population(n_beings, radius, verbose=verbose)

        self.verbose = False

    def run_algorithm(self,
                      max_epochs: int = 10,
                      verbose: bool = False
                      ) -> None:
        """
        Запускает алгоритм.
        :param max_epochs: Максимальное количество эпох алгоритма.
        :param verbose: Выводить ли информацию об обучении.
        """
        self.population.fitness(self.ALPHA, self.BETA, self.GAMMA)

        for epoch in range(1, max_epochs + 1):
            if len(self.population) == 0:
                break

            print(f'epoch #{epoch} started')

            t0 = time.perf_counter()

            self.population.select(self.SURVIVE_RATE)
            t_select = time.perf_counter()

            self.population.crossover()  # TODO: дебажим кроссовер, видимо
            t_crossover = time.perf_counter()

            self.population.mutate(remove_rate=self.REMOVE_RATE, move_rate=self.MOVE_RATE)
            t_mutate = time.perf_counter()

            self.population.fitness(self.ALPHA, self.BETA, self.GAMMA)
            if verbose:
                print('-=time consumption=-')
                print(f'select: {t_select - t0}')
                print(f'crossover: {t_crossover - t_select}')
                print(f'mutate: {t_mutate - t_crossover}')

                max_metric = self.ALPHA + self.BETA + self.GAMMA
                self.population.beings.sort(key=lambda being: being.fitness,
                                            reverse=True)
                best = self.population.beings[0]
                print(
                    f'best_fitness={best.fitness} / {max_metric}; has_circles={len(best.circles)}; n_beings={len(self.population)}')
        if verbose:
            print('done!')

    def get_best(self):
        """Возвращает результат работы алгоритма - многоугольники, приближающие искомые круги."""
        if len(self.population) == 0:
            raise Exception("Unable to get best being: population is empty!")
        self.population.fitness(self.ALPHA, self.BETA, self.GAMMA)
        self.population.beings.sort(key=lambda being: being.fitness,
                                    reverse=True)
        best = self.population.beings[0]
        return best.circles

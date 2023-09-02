import random
from collections import defaultdict
import numpy as np
from shapely import Polygon, Point, LineString
from shapely.ops import unary_union, linemerge, polygonize
import math
import scipy.optimize as optimize
from scipy.spatial import Voronoi
from Utils.misc_funcs import group_n, point_inside_polygon
import time

# CONSTANTS
CIRCLE_RESOLUTION = 100
EPS = 1e-7


# END CONSTANTS

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


class Population():
    """Описывает популяцию."""

    def __init__(self,
                 polygon: Polygon,
                 init_circles: int):
        self.polygon = polygon
        self.beings = []
        self.init_circles = init_circles  # TODO: сколько окружностей должно быть как максимум?

    def fill_population(self,
                        n_beings: int,
                        radius: float,
                        verbose: bool) -> None:
        """
        Заполняет популяцию особями.
        :param n_beings: Количество особей.
        :param radius: Радиус кругов особей.
        """
        if verbose:
            print("filling population:")
        for i in range(n_beings):
            t0 = time.perf_counter()
            self.beings.append(self._create_being(radius, verbose=verbose))
            t1 = time.perf_counter()
            if verbose:
                print(f'being {i + 1} created in {t1 - t0} sec')

    def fitness(self, ALPHA: float, BETA: float, GAMMA: float):
        """
        Вычисляет фитнес-функцию для особей.
        """
        for being in self.beings:
            outside = 0
            self_inter = 0
            for circle in being.circles:
                outside += circle.area - being.polygon.intersection(circle.polygon).area
                without = [c.polygon for c in being.circles if c != circle]
                self_inter += unary_union(without).intersection(circle.polygon).area / circle.area

            outside /= being.polygon.area
            self_inter /= unary_union([c.polygon for c in being.circles]).area
            circle_count = len(being.circles) / self.init_circles
            being.fitness = (ALPHA * (1 - self_inter) +
                             BETA * (1 - outside) +
                             GAMMA * (1 - circle_count))

    def select(self,
               survive_rate: float) -> None:
        """
        Моделирует естественный отбор.
        :param survive_rate: Доля выживающих особей.
        """
        survive_count = int(len(self.beings) * survive_rate)
        self.beings.sort(key=lambda being: being.fitness,
                         reverse=True)
        self.beings = self.beings[:survive_count]

    def crossover(self):
        to_add = []
        for _ in range((len(self.beings) + 1) // 2):
            being1 = random.choice(self.beings)
            being2 = random.choice(self.beings)

            children = self._breed(being1, being2)
            to_add.extend(children)
        self.beings.extend(to_add)

    def _breed(self, being1: 'Being', being2: 'Being') -> list['Being']:
        def breed1to2(being1: 'Being', being2: 'Being') -> 'Being':
            """Применяет скрещивание второй особи к первой."""
            circles = []  # TODO: для разных радиусов придётся использовать взвешенного Вороного - в scipy вроде его нет
            for (i, cell) in self._get_voronoi_polygons(being1):
                if random.randint(0, 1) == 0:
                    circles.append(being1.circles[i])
                else:
                    cur_circles = [c for c in being2.circles if cell.contains(c.center)]
                    if cur_circles == []:
                        circles.append(being1.circles[i])
                    else:
                        circles.extend(cur_circles)

            being = Being.from_circles(being1.polygon, circles)
            return self._repair_being(being)

        children = []
        child1 = breed1to2(being1, being2)
        if child1.covers_polygon:
            children.append(child1)

        child2 = breed1to2(being2, being1)
        if child2.covers_polygon:
            children.append(child2)
        return children

    def _get_voronoi_polygons(self, being: 'Being'):
        """
        Возвращает пары (индекс круга, ячейка диаграммы Вороного) для переданной особи.
        """

        def multicircle_case(being: 'Being'):
            """
            Вспомогательная функция.
            Обрезает бесконечные ячейки диаграммы Вороного.

            :return: Список пар (индекс круга, соответствующая ячейка типа Polygon).
            """
            (minx, miny, maxx, maxy) = being.polygon.bounds
            diameter = np.sqrt((maxx - minx) ** 2 + (maxy - miny) ** 2)

            vor = Voronoi([np.array([c.center.x, c.center.y]) for c in being.circles])

            # Заранее выясним направление каждой бесконечной грани.
            centroid = vor.points.mean(axis=0)

            # Ключ имеет вид (p, v) хранит направляющие векторы для бесконечных граней
            # Вороного, выходящих из точки диаграммы с индексом v, для ячейки, центром которой
            # является точка с индексом p
            ridge_direction = defaultdict(list)
            for (p, q), rv in zip(vor.ridge_points, vor.ridge_vertices):
                u, v = sorted(rv)
                if u == -1:  # Бесконечная грань Вороного.
                    t = vor.points[p] - vor.points[q]  # Вектор pq.
                    n = np.array([-t[1], t[0]]) / np.linalg.norm(t)  # Нормаль к pq.
                    mid = vor.points[[p, q]].mean(axis=0)
                    # Повернём нормаль в сторону от центроида многоугольника.
                    dir = n * np.sign(np.dot(n, mid - centroid))
                    ridge_direction[p, v].append(dir)
                    ridge_direction[q, v].append(dir)

            # Построим ячейки.
            ans = []
            for i, r in enumerate(vor.point_region):
                region = vor.regions[r]

                if -1 not in region:
                    #  Ячейка конечна.
                    ans.append((i, Polygon(vor.vertices[region])))
                    continue

                # Ячейка бесконечна.
                ind = region.index(-1)
                prev = region[(ind - 1) % len(region)]
                next = region[(ind + 1) % len(region)]

                if prev == next:
                    # В этой ячейке две бесконечных грани Вороного выходят
                    # из одной точки.
                    dir_prev, dir_next = ridge_direction[i, prev]
                else:
                    (dir_prev,) = ridge_direction[i, prev]
                    (dir_next,) = ridge_direction[i, next]

                length_coef = 2 * diameter / np.linalg.norm(dir_prev + dir_next)

                new_edge = np.array([
                    vor.vertices[prev] + dir_prev * length_coef,
                    vor.vertices[next] + dir_next * length_coef
                ])
                cell_points = np.concatenate((vor.vertices[region[:ind]],
                                              new_edge,
                                              vor.vertices[region[ind + 1:]]),
                                             axis=0)
                ans.append((i, Polygon(cell_points)))
            return ans

        if len(being.circles) == 0:
            return []
        if len(being.circles) == 1:
            return [(0, being.polygon)]
        elif len(being.circles) == 2:
            p1 = being.circles[0].center
            p2 = being.circles[1].center
            m = Point((p1.x + p2.x) / 2, (p1.y + p2.y) / 2)

            k0 = (p2.y - p1.y) / (p2.x - p1.x)
            k = -1 / k0
            b = m.y - k * m.x
            perp_line = lambda x: k * x + b  # Надеемся, что в вещественных числах не существует вертикальных прямых.

            (minx, miny, maxx, maxy) = being.polygon.bounds

            lx = minx - 5
            rx = maxx + 5
            pt3 = Point(lx, perp_line(lx))
            pt4 = Point(rx, perp_line(rx))

            pline = LineString([pt3, pt4])

            merged = linemerge(being.polygon.boundary, pline)
            borders = unary_union(merged)
            polygons = list(polygonize(borders))

            if polygons[0].contains(p1):
                return [(i, polygons[i]) for i in range(2)]
            else:
                return [(1 - i, polygons[i]) for i in range(2)]
        else:
            tmp = multicircle_case(being)
            return [(i, being.polygon.intersection(cell)) for (i, cell) in tmp]

    def mutate(self,
               remove_rate: float,
               move_rate: float):
        to_add = []

        minx, miny, maxx, maxy = self.polygon.bounds
        width = maxx - minx
        height = maxy - miny

        for being in self.beings:
            # Remove:
            if len(being.circles) > 1 and random.random() < remove_rate:
                being.circles.sort(key=lambda circle: circle.polygon.intersection(self.polygon).area)
                being1 = Being.from_circles(being.polygon, being.circles[1:])
                being1 = self._repair_being(being1)
                if being1.covers_polygon:
                    to_add.append(being1)

                being.circles.sort(
                    key=lambda circle:
                    sum([c2.polygon.intersection(circle.polygon) for c2 in
                         being.circles]))  # TODO: проверить на корректность
                being2 = Being.from_circles(being.polygon, being.circles[:-1])
                being2 = self._repair_being(being2)
                if being2.covers_polygon:
                    to_add.append(being2)

            # Move:
            if len(being.circles) > 0 and random.random() < move_rate:
                being1 = Being.from_circles(being.polygon, being.circles[:])
                circle_ind = random.randrange(len(being.circles))

                dx = random.uniform(-width, width)  # TODO: выбрать распределение случайной величины?
                dy = random.uniform(-height, height)
                c = being1.circles[circle_ind]

                being1.circles[circle_ind] = Circle(
                    Point(c.center.x + dx, c.center.y + dy),
                    c.radius)

                being1 = self._repair_being(being1)
                if being1.covers_polygon:
                    to_add.append(being1)

    def __len__(self):
        return len(self.beings)

    def _create_being(self, radius: float, verbose: bool):
        """
        Возвращает гарантированно корректную особь.
        :param radius: Радиус кругов особи.
        """
        while True:
            being = Being(self.polygon, radius, n_circles=self.init_circles)
            being = self._repair_being(being)
            if being.covers_polygon:
                if verbose:
                    print("Created successfully")
                return being
            elif verbose:
                print("Failed to create. Trying again...")

    def _repair_being(self, being: 'Being') -> 'Being':  # TODO: переделать для набора с разными радиусами
        """
        Пытается увеличить площадь покрытия многоугольника для данной особи.
        :param being: Особь.
        :return: Новая особь.
        """
        # TODO: fix problem when zero circles
        radius = being.circles[0].radius if len(being.circles) else 0
        tupled = [(c.center.x, c.center.y) for c in being.circles]
        initial = np.array([item for pair in tupled for item in pair])

        #print("started minimization")
        minimum = optimize.minimize(
            self._bfgs_target_func,
            initial,  # TODO: type mismatch. will it work? list instead of ndarray
            args=(being.polygon, radius),
            method='L-BFGS-B',
            options={'gtol': 1e-6, 'disp': False})
        #print("ended minimization")

        new_being = Being.from_circles(
            polygon=being.polygon,
            circles=[Circle(Point(c[0], c[1]), radius) for c in group_n(2, minimum.x)])

        return self._remove_unnec_circles(new_being, 0.05, 0.05)

    def _bfgs_target_func(self,
                          centers,
                          polygon,
                          radius):  # TODO: переделать для набора с разными радиусами
        """Целевая функция, оптимизируемая алгоритмом BFGS."""
        circles = [Circle(Point(c[0], c[1]), radius).polygon for c in group_n(2, centers)]
        ar = unary_union(circles).intersection(polygon).area
        s = 3
        soft_inv = 1 / ((1 + (ar ** s)) ** (1 / s))

        return soft_inv

    def _remove_unnec_circles(self,
                              being: 'Being',
                              thr_region: float,
                              thr_self: float) -> 'Being':  # TODO: перепроверить, не доверяю ему
        """
        Удаляет мало полезные круги.

        :param being: Особь, для которой происходит удаление.
        :param thr_region: Минимальная доля площади круга, которая должна покрывать многоугольник.
        :param thr_self: Минимальная допустимая доля площади пересечения с другими кругами. (см. код для уточнения)
        :return: Особь с обновлённым набором кругов.
        """
        # TODO: ПЕРЕЧИТАТЬ ВНИМАТЕЛЬНО
        kept_circles = []
        for circle in being.circles:
            rate = circle.polygon.intersection(
                being.polygon).area / circle.area  # TODO: circle.polygon.intersect -> circle.intersect
            if rate >= thr_region:
                kept_circles.append(circle)

        circle_list = kept_circles
        kept_circles, removed_circles = [], []
        for circle in circle_list:
            tmp = [
                c.polygon
                for c in circle_list
                if (c not in removed_circles) and (c != circle)
            ]
            rate = np.abs(unary_union(tmp).intersection(circle.polygon).area - circle.area) / circle.area
            if rate >= thr_self:
                kept_circles.append(circle)
            else:
                removed_circles.append(circle)

        return Being.from_circles(being.polygon, kept_circles)


class Being():
    def __init__(self,
                 polygon: Polygon,
                 radius: float,
                 circles=None,
                 n_circles=None):  # TODO: поправить этот конструктор и from_circles, его проблемы с безопасностью: не гарпантирует корректнрость особи

        self.fitness = None  # Значение фитнес-функции.
        self.polygon = polygon
        if circles == None:
            self.circles = [Circle(point_inside_polygon(polygon), radius) for _ in range(n_circles)]
        else:
            self.circles = circles

    @property
    def covers_polygon(self):
        """Важно: Работает не слишком быстро, не стоит злоупотреблять."""
        inter = unary_union([c.polygon for c in self.circles]).intersection(self.polygon)
        return np.abs(inter.area - self.polygon.area) < EPS

    @classmethod
    def from_circles(cls,
                     polygon: Polygon,
                     circles: list['Circle']) -> 'Being':
        return cls(polygon, 1, circles)


class Circle():
    def __init__(self,
                 center: Point,
                 radius: float):
        self.center = center
        self.radius = radius

        points = []
        for i in range(CIRCLE_RESOLUTION):
            theta = 2 * math.pi * i / CIRCLE_RESOLUTION
            x = center.x + radius * math.cos(theta)
            y = center.y + radius * math.sin(theta)
            points.append(Point(x, y))

        self.polygon = Polygon(points)
        self.area = self.polygon.area

    @property
    def exterior(self):
        """
        Возвращает внешнюю границу круга.
        :return: Многоугольник, приближающий внешнюю границу круга.
        """
        return self.polygon.exterior

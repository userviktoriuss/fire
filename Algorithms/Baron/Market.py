import random

from Utils.Circle import *
from Algorithms.Baron.Baron import Baron
from collections import defaultdict
from Utils.misc_funcs import point_inside_polygon, sign
from shapely.ops import unary_union, nearest_points
import math

EPS = 1e-8


class Market:
    def __init__(self,
                 polygon: Polygon,
                 grid_size: float):
        self.polygon = polygon
        self.grid = defaultdict(list)
        self.grid_size = grid_size

    def fill_barons(self,
                    n_barons: int,
                    radius: float):
        #random.seed(42)
        for i in range(n_barons):
            c = point_inside_polygon(self.polygon)
            baron = Baron(c, radius)
            crds = self.grid_cords(c)
            self.grid[crds].append(baron)

    def next_iteration(self,
                       tau: float,
                       regular_mult: float,
                       half_mult: float,
                       far_mult: float,
                       covered_mult: float):
        deltas = []

        for cords in self.grid:
            for baron in self.grid[cords]:
                uncovered = Polygon(baron.polygon)
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        cur = (cords[0] + dx, cords[1] + dy)
                        if cur not in self.grid:
                            continue

                        for b in self.grid[cur]:
                            if b == baron:
                                continue
                            uncovered = uncovered.difference(b.polygon)

                # TODO: можно как вариант работы добавлять круги, если не хватает, и удалять, если круг оказался за границей. Так будет происходить самокорректировка алгоритма. Мб он даже в конце сойдётся
                if uncovered.area > EPS:
                    if self.polygon.contains(baron.center):
                        # Внутри многоугольника и пересекается с кем-то.
                        deltas.append(((uncovered.centroid.x - baron.center.x) * regular_mult,
                                       (uncovered.centroid.y - baron.center.y) * regular_mult))
                    elif math.fabs(uncovered.area - baron.polygon.area) > EPS:
                        # Пересекается с кем-то, но не полностью внутри многоугольника.
                        # (это могут быть два круга вне многоугольника - практически невероятная ситуация при правильных границах tau)

                        dir = Point(baron.center.x - uncovered.centroid.x,
                                    baron.center.y - uncovered.centroid.y)
                        len = math.sqrt(dir.x * dir.x + dir.y * dir.y)
                        deltas.append((dir.x / len * baron.radius / 2 * half_mult,
                                       dir.y / len * baron.radius / 2 * half_mult))
                    else:
                        # Полностью снаружи и не пересекается.
                        p, _ = nearest_points(self.polygon, baron.center)
                        dir = Point(p.x - baron.center.x,
                                    p.y - baron.center.y)
                        length = math.sqrt(dir.x * dir.x + dir.y * dir.y)
                        deltas.append(
                            (dir.x * baron.radius / length * far_mult,
                             dir.y * baron.radius / length * far_mult))
                else:
                    # Полностью покрыт. Сдвинем случайно.
                    length = random.uniform(0, baron.radius)
                    theta = random.uniform(0, 2 * math.pi)
                    x = length * math.cos(theta) * covered_mult
                    y = length * math.sin(theta) * covered_mult
                    deltas.append((x, y))

        i = 0
        for cords in self.grid:
            for baron in self.grid[cords]:
                baron.move(deltas[i][0] * tau, deltas[i][1] * tau)
                i += 1

    def grid_cords(self, A: Point):
        x = sign(A.x) * math.fabs(A.x) // self.grid_size
        y = sign(A.y) * math.fabs(A.y) // self.grid_size
        return (x, y)

import random

from Utils.Circle import *
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
        for i in range(n_barons):
            c = point_inside_polygon(self.polygon)
            baron = Baron(c, radius)  # TODO: пронаследовать Baron от Circle
            crds = self.grid_cords(c)
            self.grid[crds].append(baron)

    def next_iteration(self, tau: float):
        deltas = []

        for (cords, cell) in self.grid:
            for baron in cell:
                uncovered = Polygon(baron.polygon)
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        for b in self.grid[cords[0] + dx, cords[1] + dy]:
                            if b == baron:
                                continue
                            uncovered = uncovered.difference(b.polygon)

                # TODO: корректируем, если круг вышел за границу
                # TODO: можно как вариант работы добавлять круги, если не хватает, и удалять, если круг оказался за границей. Так будет происходить самокорректировка алгоритма. Мб он даже в конце сойдётся

                if uncovered.area > EPS:  # TODO: перепроверить.
                    if self.polygon.contains(baron.center):
                        # Внутри многоугольника и пересекается с кем-то.
                        dir = uncovered.centroid - baron.center
                        deltas.append((dir.x, dir.y))
                    elif math.fabs(uncovered.area - baron.polygon.area) > EPS:
                        # Пересекается с кем-то, но не внутри многоугольника.
                        # (это могут быть два круга вне многоугольника - практически невероятная ситуация при правильных границах tau)
                        covered = baron.polygon.difference(uncovered)
                        dir = covered.centroid - baron.center  # Так он должен чуть быстрее оказываться внутри.
                        deltas.append((dir.x, dir.y))
                    else:
                        # Полностью снаружи и не пересекается.
                        p, _ = nearest_points(self.polygon, baron.center)
                        dir = p - baron.center
                        length = math.sqrt(dir.x * dir.x + dir.y * dir.y)
                        deltas.append(
                            (dir.x * baron.radius / length,
                             dir.y * baron.radius / length))
                else:
                    # Полностью покрыт. Сдвинем случайно.
                    length = random.uniform(0, baron.radius)
                    theta = random.uniform(0, 2 * math.pi)
                    x = length * math.cos(theta)
                    y = length * math.sin(theta)
                    deltas.append((x, y))

        i = 0
        for (cords, cell) in self.grid:
            for baron in cell:
                baron.move(deltas[i][0] * tau, deltas[i][1] * tau)
                i += 1



    def grid_cords(self, A: Point):
        x = sign(A.x) * math.fabs(A.x) // self.grid_size
        y = sign(A.y) * math.fabs(A.y) // self.grid_size
        return (x, y)

import time
from matplotlib import pyplot as plt
from shapely import Point, Polygon

from Algorithms.BranchesAndBounds.BranchesAndBounds import bnb
from Algorithms.Halton.Halton import halton
from Algorithms.Hexagonal.hexagonal import HexagonalAlgorithm
from Examples.polygons import polygons_dict
from Utils.Circle import Circle
from Utils.drawing import draw_polygon, draw_circles

P = polygons_dict['P8']
# Запуск алгоритма
t0 = time.perf_counter()
(minx, miny, maxx, maxy) = P.bounds
P_described = Polygon([Point(minx - 1, miny - 1), Point(maxx + 1, miny - 1), Point(maxx + 1, maxy + 1), Point(minx - 1, maxy + 1)])
centers = halton(
    P=P_described,
    n_points=70,
    p1=11,
    p2=7,
    start=383,
    step=389,
)
ans = [Circle(c, 1) for c in centers if P.contains(c)]
t1 = time.perf_counter()
bnb_grid = bnb(P, ans,
               ALPHA=0.3,
               BETA=0.3,
               GAMMA=0,
               LAMBDA=1.5,
               MOVE_SCHEDULE=lambda x: x * 0.995,
               is_repaired=True)

t2 = time.perf_counter()

# Выведем числовые результаты работы.
print(f'Inner time: {t1 - t0} sec.')
print(f'BnB time: {t2 - t1} sec.')
print(f'Elapsed time: {t2 - t0} sec.')
print(f'Inner result: {len(ans)} circles')
print(f'BnB results:  {len(bnb_grid)} circles.')

fig, ax = plt.subplots(nrows=1, ncols=2)
# Отрисуем результат до запуска внутреннего алгоритма.
ax[0].set_aspect('equal', adjustable='box')
draw_polygon(ax[0], P)
draw_circles(ax[0], ans)

# Отрисуем результат после запуска внутреннего алгоритма.

ax[1].set_aspect('equal', adjustable='box')
draw_polygon(ax[1], P)
draw_circles(ax[1], bnb_grid)

plt.show()


"""
import time
from matplotlib import pyplot as plt
from Algorithms.BranchesAndBounds.BranchesAndBounds import bnb
from Algorithms.Hexagonal.hexagonal import HexagonalAlgorithm
from Examples.polygons import polygons_dict
from Utils.drawing import draw_polygon, draw_circles

P = polygons_dict['P8']
# Запуск алгоритма
t0 = time.perf_counter()

alg = HexagonalAlgorithm(P, 1)  # Укажем данные.
alg.set_params()  # Укажем параметры решения.
alg.run_algorithm()  # Запустим алгоритм.
ans = alg.get_result()  # Получим результат - list[Circle].

bnb_grid = bnb(P, ans, is_repaired=True)

t1 = time.perf_counter()

# Выведем числовые результаты работы.
print(f'Elapsed time: {t1 - t0} sec.')
print(f'Inner result: {len(ans)} circles')
print(f'BnB results:  {len(bnb_grid)} circles.')

fig, ax = plt.subplots(nrows=1, ncols=2)
# Отрисуем результат до запуска внутреннего алгоритма.
ax[0].set_aspect('equal', adjustable='box')
draw_polygon(ax[0], P)
draw_circles(ax[0], ans)

# Отрисуем результат после запуска внутреннего алгоритма.

ax[1].set_aspect('equal', adjustable='box')
draw_polygon(ax[1], P)
draw_circles(ax[1], bnb_grid)

plt.show()

"""
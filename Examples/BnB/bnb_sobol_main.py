import time
from matplotlib import pyplot as plt
from shapely import Point, Polygon

from Algorithms.BranchesAndBounds.BranchesAndBounds import bnb
from Algorithms.Halton.Halton import halton
from Algorithms.Hexagonal.hexagonal import HexagonalAlgorithm
from Algorithms.Sobol.Sobol import sobol
from Examples.polygons import polygons_dict
from Utils.Circle import Circle
from Utils.drawing import draw_polygon, draw_circles

P = polygons_dict['P8']
# Запуск алгоритма
t0 = time.perf_counter()
ans = sobol(
    P=P,
    n_points=64)
t1 = time.perf_counter()
bnb_grid = bnb(P, ans,
               max_iterations=40,
               ALPHA=0.5,
               BETA=0.3,
               GAMMA=0.3,
               LAMBDA=5,
               MOVE_SCHEDULE=lambda x: x,
               DELETE_PROB=0.1,
               is_repaired=True,
               remove_unnecessary=True)

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


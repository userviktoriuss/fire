import time
from matplotlib import pyplot as plt
from Algorithms.BranchesAndBounds.BranchesAndBounds import bnb
from Algorithms.Hexagonal.HexagonalAlgorithm import HexagonalAlgorithm
from Examples.polygons import polygons_dict
from Utils.drawing import draw_polygon, draw_circles

P = polygons_dict['P3']
# Запуск алгоритма
t0 = time.perf_counter()

alg = HexagonalAlgorithm(P, 1)  # Укажем данные.
alg.set_params()  # Укажем параметры решения.
alg.run_algorithm()  # Запустим алгоритм.
ans = alg.get_result()  # Получим результат - list[Circle].
t1 = time.perf_counter()
bnb_grid = bnb(P,
               ans,
               max_iterations=10,
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

import time

import numpy as np
from matplotlib import pyplot as plt
from Algorithms.BranchesAndBounds.BranchesAndBounds import BnBAlgorithm
from Algorithms.Hexagonal.hexagonal import HexagonalAlgorithm
from Algorithms.NBodies.GravityFunctions import smooth_gravity_on_region_with_sign
from Algorithms.NBodies.RungeKuttaAlgorithm import RungeKuttaAlgorithm
from Examples.polygons import polygons_dict
from Utils.drawing import draw_polygon, draw_circles
from Utils.layering import get_layers

P = polygons_dict['P9']
R = 1  # Радиус.
INNER_BOUND = 2  # Начиная с этого слоя по удалению от внешних границ многоугольника круг считается внутренним.

# Построим покрытие шестиугольной сеткой.
t0 = time.perf_counter()

hex_alg = HexagonalAlgorithm(P, R)  # Укажем данные.
hex_alg.set_params()  # Укажем параметры решения.
hex_alg.run_algorithm()  # Запустим алгоритм.
hex_ans = hex_alg.get_result()  # Получим результат - list[Circle].

t1 = time.perf_counter()

# Разложим круги по уровням дальности до края многоугольника
layers = get_layers(P, hex_ans)

# Выделим "внутренние" круги.
inners = np.zeros(len(layers))
inners[layers >= INNER_BOUND] = 1

t2 = time.perf_counter()

# Починим методом ветвей и границ
bnb_alg = BnBAlgorithm(P, hex_ans)
bnb_alg.set_params(
    max_iterations=15,
    fixed=list(inners)  # TODO: пофиксить костыль с типами
)
bnb_alg.run_algorithm()
bnb_grid = bnb_alg.get_result()

t3 = time.perf_counter()

# Придвинем поближе внешние круги с помощью метода Рунге-Кутта.
rk_alg = RungeKuttaAlgorithm(
    [c.center for c in bnb_grid],
    R)
rk_alg.set_params(
    fixed=bnb_alg.fixed,  # TODO: другие параметры???,
    STOP_RADIUS=1.6 * R,
    TIME_STOP=10,
    gravity=smooth_gravity_on_region_with_sign
)
rk_alg.run_algorithm()
rk_ans = rk_alg.get_result()

t4 = time.perf_counter()

# Выведем числовые результаты работы.
print(f'Hex creation time: {t1 - t0} sec.')
print(f'Get layers time: {t2 - t1} sec.')
print(f'BnB time: {t3 - t2} sec.')
print(f'Runge-Kutta time: {t4 - t3} sec.')
print(f'Elapsed time: {t4 - t0} sec.')
print(f'Before BnB result: {len(hex_ans)} circles')
print(f'BnB results:  {len(bnb_grid)} circles.')

fig, ax = plt.subplots(nrows=1, ncols=3)
# Отрисуем результат построения сетки.
ax[0].set_aspect('equal', adjustable='box')
draw_polygon(ax[0], P)
draw_circles(ax[0], hex_ans)

# Отрисуем результат после запуска метода Рунге-Кутта
ax[1].set_aspect('equal', adjustable='box')
draw_polygon(ax[1], P)
draw_circles(ax[1], bnb_grid)

# Отрисуем результат после запуска метода ветвей и границ.
ax[2].set_aspect('equal', adjustable='box')
draw_polygon(ax[2], P)
draw_circles(ax[2], [rk_ans[i] for i in range(len(rk_ans)) if not rk_alg.fixed[i]])
draw_circles(ax[2],
             [rk_ans[i] for i in range(len(rk_ans)) if rk_alg.fixed[i]],
             'red',
             'darkred')

plt.show()

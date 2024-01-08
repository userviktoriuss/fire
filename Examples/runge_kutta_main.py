import time

import numpy.random
from matplotlib import pyplot as plt
from numpy.random import randint
from shapely import Point

from Algorithms.NBodies.RungeKuttaAlgorithm import RungeKuttaAlgorithm
from Examples.polygons import polygons_dict
from Utils.Circle import Circle
from Utils.drawing import draw_polygon, draw_circles

# Выбор многоугольника
P = polygons_dict['P3']

# Подготовка алгоритма
t0 = time.perf_counter()

numpy.random.seed(42)
centers = [Point(randint(-5, 5), randint(-5, 5)) for i in range(10)]
alg = RungeKuttaAlgorithm(centers, 1.5)  # Укажем данные.
alg.set_params(
    fixed=[0, 1, 1, 1, 0, 0, 0, 0, 0, 0]
    # fixed=[0, 1, 1, 1, 0, 0, 0, 0, 0, 0]
)  # Укажем параметры решения.
# Запуск алгоритма
t1 = time.perf_counter()
alg.run_algorithm()  # Запустим алгоритм.

ans = alg.get_result()  # Получим результат - list[Circle].

t2 = time.perf_counter()

# Выведем числовые результаты работы.
print(f'Preparation time: {t1 - t0} sec.')
print(f'Algorithm time: {t2 - t1} sec.')
print(f'Elapsed time: {t2 - t0} sec.')

fig, ax = plt.subplots(nrows=1, ncols=2)
# Отрисуем результат до запуска внутреннего алгоритма.
ax[0].set_aspect('equal', adjustable='box')
draw_polygon(ax[0], P)

# Нарисуем разными цветами зафиксированные и незафиксированные круги.
draw_circles(ax[0],
             [Circle(centers[i], 1.5) for i in range(len(alg.fixed)) if
              not alg.fixed[i]])  # TODO: отрисовывать, что было до

draw_circles(ax[0],
             [Circle(centers[i], 1.5) for i in range(len(alg.fixed)) if alg.fixed[i]],
             color='red',
             center_color='darkred')

# Отрисуем результат после запуска внутреннего алгоритма.
ax[1].set_aspect('equal', adjustable='box')
draw_polygon(ax[1], P)
# Нарисуем разными цветами зафиксированные и незафиксированные круги.
draw_circles(ax[1],
             [ans[i] for i in range(len(alg.fixed)) if not alg.fixed[i]])
draw_circles(ax[1],
             [ans[i] for i in range(len(alg.fixed)) if alg.fixed[i]],
             color='red',
             center_color='darkred')

plt.show()

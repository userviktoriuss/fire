import time

import numpy.random
from matplotlib import pyplot as plt

from Algorithms.NBodies.GravityFunctions import repel_cut_gravity
from Algorithms.NBodies.Loggers.RKAnimationLogger import RKAnimationLogger
from Algorithms.NBodies.RundeKuttaWithPolygonAlgorithm import RungeKuttaWithPolygonAlgorithm
from Examples.polygons import polygons_dict
from Utils.Circle import Circle
from Utils.drawing import draw_polygon, draw_circles

# Выбор многоугольника
from Utils.misc_funcs import point_inside_polygon

name = 'P4'  # Название многоугольника
k = 29  # Ожидаемое количество кругов, необходимое для покрытия.
P = polygons_dict[name]

# Подготовка алгоритма
t0 = time.perf_counter()

numpy.random.seed(42)
centers = [point_inside_polygon(P) for i in range(k)]

logger = RKAnimationLogger(P)
logger.reset(xlim=(-1, 20), ylim=(-1, 10))

alg = RungeKuttaWithPolygonAlgorithm(P, centers, 1.5)  # Укажем данные.
alg.set_params(
    fixed=[0 for i in range(k)],
    G=0.2,  # 0.2,  # 0.1
    poly_G_out=10,
    poly_G_in=0.15,  # 0.2,  # 0.3
    gravity=repel_cut_gravity,
    logger=logger
)  # Укажем параметры решения.
# Запуск алгоритма
t1 = time.perf_counter()
alg.run_algorithm()  # Запустим алгоритм.

ans = alg.get_result()  # Получим результат - list[Circle].

logger.save_log(f'{name}_rk_log_{alg.G}_{alg.poly_G_out}_{alg.poly_G_in}.gif')

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

import logging
import time

import matplotlib.pyplot as plt

from Algorithms.NBodies.GravityFunctions import repel_cut_gravity
from Algorithms.NBodies.RundeKuttaWithPolygonAlgorithm import RungeKuttaWithPolygonAlgorithm
from Algorithms.Sobol.Sobol import sobol
from Examples.polygons import polygons_dict
from Utils.drawing import draw_polygon, draw_circles
from Utils.misc_funcs import expected_circle_count_weighted

R = 1.5
P = polygons_dict['P7']

t0 = time.perf_counter()
expected_circles = expected_circle_count_weighted(P, R)

logger = logging.getLogger('sobol')
logging.basicConfig(filename='myapp.log', level=logging.INFO)
logger.info('Expect %d circles', expected_circles)
centers = [c.center for c in sobol(P, expected_circles, R)]

t1 = time.perf_counter()
alg = RungeKuttaWithPolygonAlgorithm(P, centers, R)  # Укажем данные.
alg.set_params(
    fixed=[0 for _ in range(len(centers))],
    gravity=repel_cut_gravity,
    G=0.2,
    poly_G_out=10,
    poly_G_in=0.15,  # 0.2,  # 0.3
)  # Укажем параметры решения.
# Запуск алгоритма

alg.run_algorithm()  # Запустим алгоритм.

ans = alg.get_result()

t2 = time.perf_counter()

print(f'Sobol time: {t1 - t0} sec.')
print(f'RK time: {t2 - t1} sec.')
print(f'Elapsed time: {t2 - t0} sec.')

ax = plt.gca()
ax.set_aspect('equal', adjustable='box')

draw_polygon(ax, P)
draw_circles(ax, ans)

plt.show()


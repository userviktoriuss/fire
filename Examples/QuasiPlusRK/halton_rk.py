import logging
import time

from Algorithms.Halton.Halton import halton
import matplotlib.pyplot as plt

from Algorithms.NBodies.GravityFunctions import repel_cut_gravity
from Algorithms.NBodies.RundeKuttaWithPolygonAlgorithm import RungeKuttaWithPolygonAlgorithm
from Examples.polygons import polygons_dict
from Utils.drawing import draw_polygon, draw_circles
from Utils.misc_funcs import expected_circle_count_weighted

R = 1.5
P = polygons_dict['P9']

t0 = time.perf_counter()
expected_circles = expected_circle_count_weighted(P, R)

logger = logging.getLogger('halton')
logging.basicConfig(filename='myapp.log', level=logging.INFO)
logger.info('Expect %d circles', expected_circles)

centers = halton(
    P=P,
    margin=0,
    n_points=expected_circles,
    p1=2,
    p2=3,
    start=1,
    step=1,
)

t1 = time.perf_counter()
alg = RungeKuttaWithPolygonAlgorithm(P, centers, R)  # Укажем данные.
alg.set_params(
    fixed=[0 for _ in range(len(centers))],
    gravity=repel_cut_gravity,
    G=0.2,
    poly_G_out=10,
    poly_G_in=0.15,  # 0.2,  # 0.3
)  # Укажем параметры решения.
alg.run_algorithm()
ans = alg.get_result()
#ans = list(filter(lambda c: P.contains(c.center), ans))

t2 = time.perf_counter()

print(f'Halton time: {t1 - t0} sec.')
print(f'RK time: {t2 - t1} sec.')
print(f'Elapsed time: {t2 - t0} sec.')

ax = plt.gca()
ax.set_aspect('equal', adjustable='box')

draw_polygon(ax, P)
draw_circles(ax, ans)

plt.show()


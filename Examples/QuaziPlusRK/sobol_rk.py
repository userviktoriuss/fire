import time

import matplotlib.pyplot as plt

from Algorithms.NBodies.GravityFunctions import smooth_gravity_on_region_with_sign
from Algorithms.NBodies.RungeKuttaAlgorithm import RungeKuttaAlgorithm
from Algorithms.Sobol.Sobol import sobol
from Examples.polygons import polygons_dict
from Utils.drawing import draw_polygon, draw_circles

R = 1
P = polygons_dict['P9']

t0 = time.perf_counter()
centers = [c.center for c in sobol(P, 32, R)]

t1 = time.perf_counter()
rk_alg = RungeKuttaAlgorithm(centers, R)
rk_alg.set_params(
    STOP_RADIUS=1.5 * R,
    TIME_STOP=70,
    gravity=smooth_gravity_on_region_with_sign
)
rk_alg.run_algorithm()
ans = rk_alg.get_result()

t2 = time.perf_counter()

print(f'Halton time: {t1 - t0} sec.')
print(f'RK time: {t2 - t1} sec.')
print(f'Elapsed time: {t2 - t0} sec.')

ax = plt.gca()
ax.set_aspect('equal', adjustable='box')

draw_polygon(ax, P)
draw_circles(ax, ans)

plt.show()


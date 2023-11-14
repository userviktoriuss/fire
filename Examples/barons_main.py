import math
import random
import time

from Algorithms.Baron.BaronsAlgorithm import BaronsAlgorithm
from shapely import Polygon, Point
import matplotlib.pyplot as plt

# Зародыш TDD
#P = Polygon([Point(0, 0), Point(2, 0), Point(6, 2), Point(1, 5), Point(1, 4)])
from Utils.Circle import Circle

#P = Polygon([Point(0, 0), Point(5, 0), Point(5, 5), Point(0, 5)])
#plt.plot(P.exterior.xy[0], P.exterior.xy[1])
dx = 1.5
theta = 60
hypot = dx / math.cos(theta)
dy = math.sqrt(hypot ** 2 - dx ** 2)

P = Polygon([Point(dx * k / 10, (dx * k / 10) ** 6) for k in range(10)] + [Point(0.5 * dx, (0.9 * dx) ** 6)])
(minx, miny, maxx, maxy) = P.bounds
P_described = Polygon([Point(minx - 1, miny - 1), Point(maxx + 1, miny - 1), Point(maxx + 1, maxy + 1), Point(minx - 1, maxy + 1)])
inners = []

for inn in inners:
    P = P.difference(inn)

t0 = time.perf_counter()
alg = BaronsAlgorithm(
    polygon=P,
    n_barons=5,
    radius=1.0,
)

alg.run_algorithm(
    init_tau=0.5,
    end_tau=1e-4,
    change_tau=0.99,
    regular_mult=1,
    half_mult=1.3,
    far_mult=1.7,
    covered_mult=1,
    verbose=True
) # avg time 32 sec

circles = alg.get_circles()

t1 = time.perf_counter()

ax = plt.gca()
ax.set_aspect('equal', adjustable='box')

plt.plot(P.exterior.xy[0], P.exterior.xy[1])

for circle in circles:
    plt.plot(circle.exterior.xy[0], circle.exterior.xy[1])

for p_int in P.interiors:
    xx = [c[0] for c in p_int.coords]
    yy = [c[1] for c in p_int.coords]
    plt.plot(xx, yy, color='tab:blue')

plt.show()

print(f'Elapsed time: {t1 - t0} sec.')
print(f'S={P.area} m^2.')

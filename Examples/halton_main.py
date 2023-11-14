import math
import random
import time

from Algorithms.Halton.Halton import halton
from shapely import Polygon, Point
import matplotlib.pyplot as plt

# Зародыш TDD
#P = Polygon([Point(0, 0), Point(2, 0), Point(6, 2), Point(1, 5), Point(1, 4)])
from Utils.Circle import Circle

#P = Polygon([Point(0, 0), Point(5, 0), Point(5, 5), Point(0, 5)])
#plt.plot(P.exterior.xy[0], P.exterior.xy[1])

P = Polygon([Point(0, 0), Point(5, 0), Point(5, 5), Point(0, 5)])
(minx, miny, maxx, maxy) = P.bounds
P_described = Polygon([Point(minx - 1, miny - 1), Point(maxx + 1, miny - 1), Point(maxx + 1, maxy + 1), Point(minx - 1, maxy + 1)])
inners = []

for inn in inners:
    P = P.difference(inn)

t0 = time.perf_counter()
centers = halton(
    P=P_described,
    n_points=30,
    p1=41,
    p2=53,
    start=1,
    step=7,
)

circles = [Circle(c, 1) for c in centers if P.contains(c)]
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

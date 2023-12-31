# from Utils.genetic_classes import GeneticAlgorithm
from shapely import Polygon, Point
import matplotlib.pyplot as plt
from Algorithms.Genetic.GeneticAlgorithm import GeneticAlgorithm
import time
import math

# Зародыш TDD
#P = Polygon([Point(0, 0), Point(2, 0), Point(6, 2), Point(1, 5), Point(1, 4)])
from Utils.Circle import Circle

#P = Circle(Point(3, 3), 3).polygon
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
alg = GeneticAlgorithm(
    polygon=P,
    init_circles=6,
    n_beings=4,
    radius=1.0,
    verbose=True
)

alg.run_algorithm(
    max_epochs=5,
    verbose=True
)

circles = alg.get_best()
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

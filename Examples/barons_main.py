import random

from Algorithms.Baron.barons_classes import BaronsAlgorithm
from shapely import Polygon, Point
import matplotlib.pyplot as plt

# Зародыш TDD
P = Polygon([Point(0, 0), Point(2, 0), Point(6, 2), Point(1, 5), Point(1, 4)])

alg = BaronsAlgorithm(
    polygon=P,
    n_barons=12,
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

plt.plot(P.exterior.xy[0], P.exterior.xy[1])
for circle in circles:
    plt.plot(circle.exterior.xy[0], circle.exterior.xy[1])
plt.show()

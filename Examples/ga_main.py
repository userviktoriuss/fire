# from Utils.genetic_classes import GeneticAlgorithm
from shapely import Polygon, Point
import matplotlib.pyplot as plt
from Algorithms.Genetic.genetic_classes import GeneticAlgorithm

# Зародыш TDD
P = Polygon([Point(0, 0), Point(2, 0), Point(6, 2), Point(1, 5), Point(1, 4)])

alg = GeneticAlgorithm(
    polygon=P,
    init_circles=20,
    n_beings=4,
    radius=1.0,
    verbose=True
)


alg.run_algorithm(
    max_epochs=5,
    verbose=True
)

circles = alg.get_best()

plt.plot(P.exterior.xy[0], P.exterior.xy[1])
for circle in circles:
    plt.plot(circle.exterior.xy[0], circle.exterior.xy[1])
plt.show()

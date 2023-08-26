# from Utils.genetic_classes import GeneticAlgorithm
from shapely import Polygon, Point
import matplotlib.pyplot as plt
from Utils.genetic_classes import GeneticAlgorithm

# Зародыш TDD
P = Polygon([Point(0, 0), Point(20, 0), Point(60, 20), Point(10, 50), Point(-10, 40)])

alg = GeneticAlgorithm(
    polygon=P,
    init_circles=100,
    n_beings=100,
    radius=1.0
)

alg.run_algorithm(
    max_epochs=10,
    verbose=True
)

circles = alg.get_best()

for circle in circles:
    plt.plot(circle)
plt.show()

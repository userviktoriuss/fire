from shapely import Polygon
from Algorithms.Genetic.GeneticAlgorithm import GeneticAlgorithm
import matplotlib.pyplot as plt

# Выпуклые многоугольники, заданные вручную
# Надо бы настроить пайплайн тестирования, чтобы всё по красоте было


p = Polygon([(40, 0), (20, 20), (-10, 20), (-10, 10), (0, 0)])

alg = GeneticAlgorithm(
    polygon=p,
    init_circles=25,
    n_beings=5,
    radius=1.0,
    verbose=True
)


alg.run_algorithm(
    max_epochs=5,
    verbose=True
)

circles = alg.get_best()

plt.plot(p.exterior.xy[0], p.exterior.xy[1])
for circle in circles:
    plt.plot(circle.exterior.xy[0], circle.exterior.xy[1])
plt.show()
import time

import numpy as np
from matplotlib import pyplot as plt
from shapely import Point

from Algorithms.Hexagonal.HexagonalAlgorithm import HexagonalAlgorithm
from Algorithms.Hexagonal.hexagonal_coverings import hexagonal_np
from Examples.polygons import polygons_dict
from Utils.Circle import Circle
from Utils.drawing import draw_polygon, draw_circles
from shapely import Polygon

P = Polygon([Point(0, 0), Point(0, 50), Point(50, 50), Point(50, 0)])#polygons_dict['P9']
R = 1.5  # Радиус.

t0 = time.perf_counter()

hex_alg = HexagonalAlgorithm(P, R)  # Укажем данные.
hex_alg.set_params(
    hex_alg=hexagonal_np,
    REMOVE_REDUNDANT=False,
    ALPHA_RESOLUTION=1,
    RESOLUTION=1
)  # Укажем параметры решения.
hex_alg.run_algorithm()  # Запустим алгоритм.
hex_ans = hex_alg.get_result()

t1 = time.perf_counter()
print(f"Elapsed time: {t1 - t0}")

fig = plt.figure()
ax = fig.gca()
# Отрисуем результат построения сетки.

ax.set_aspect('equal', adjustable='box')
draw_polygon(ax, P)
draw_circles(ax, hex_ans)

plt.show()

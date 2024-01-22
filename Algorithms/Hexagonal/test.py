import numpy as np
from matplotlib import pyplot as plt
from shapely import Point

from Algorithms.Hexagonal.hexagonal_coverings import hexagonal_np
from Examples.polygons import polygons_dict
from Utils.Circle import Circle
from Utils.drawing import draw_polygon, draw_circles

P = polygons_dict['P9']
R = 1  # Радиус.

centers = hexagonal_np(P, Point(0.7, 0), R, np.pi)
circles = [Circle(c, R) for c in centers]

fig = plt.figure()
ax = fig.gca()
# Отрисуем результат построения сетки.

ax.set_aspect('equal', adjustable='box')
draw_polygon(ax, P)
draw_circles(ax, circles)

plt.show()

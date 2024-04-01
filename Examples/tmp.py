import numpy as np
import pyautocad
from pyautocad import aDouble
from Examples.polygons import polygons_dict

acad = pyautocad.Autocad()
t = polygons_dict['P9'].exterior.xy
t = np.vstack([t[0], t[1], np.zeros(len(t[0]))]).T.flatten()
t = tuple(t)
print(t)
acad.model.AddPolyline(aDouble(t))

"""
import matplotlib.pyplot as plt

from Examples.polygons import polygons_dict
from Utils.drawing import draw_polygon



fig, ax = plt.subplots(nrows=3, ncols=3)
fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0.5)
for name in polygons_dict:
    n = int(name[1]) - 1
    curax = ax[n // 3, n % 3]

    curax.set_aspect('equal', adjustable='box')
    curax.set_title(f'{name}     S={polygons_dict[name].area:0.3f}')

    draw_polygon(curax, polygons_dict[name])

plt.show()
"""
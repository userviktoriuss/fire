import math
import time
from polygons import polygons_dict

from matplotlib import pyplot as plt
from shapely import Point, Polygon

# Main part
# TODO: дописать тестирование
RADIUS = 1
for polygon_name in polygons_dict:
    print(f'-----= Test for {polygon_name} =-----')
    P = polygons_dict[polygon_name]
    (minx, miny, maxx, maxy) = P.bounds
    P_described = Polygon([Point(minx - RADIUS, miny - RADIUS), Point(maxx + RADIUS, miny - RADIUS), Point(maxx + RADIUS, maxy + RADIUS), Point(minx - RADIUS, maxy + RADIUS)])

    t0 = time.perf_counter()

    # Запуск алгоритма

    t1 = time.perf_counter()
    print(f'Elapsed time: {t1 - t0} sec.')
    # Вывод результата
    # Сохранение картинки


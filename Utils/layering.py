"""
В этом файле описаны способы определить "внешние" и "внутренние"
круги многоугольника.
"""
from queue import Queue

import numpy as np
from shapely import Polygon

from Utils import Circle

INT_MAX = np.iinfo(np.int16).max  # Это максимальное значение (и удобная заглушка), которое будут принимать слои при адекватных входных данных.
EPS = 1e-9

# Здесь внешние круги - круги, имеющие общую площадь с областью
# вне многоугольника.
def get_layers(P: Polygon, circles: list[Circle]) -> np.array:
    """
    Реализует подход определения внешних и внутренних кругов через слои.

    Возвращает список с номером слоя каждого круга для заданного
    набора кругов и многоугольника.

    :param P: Многоугольник.
    :param circles: Список кругов.
    :return: Numpy-массив целых чисел.
    """
    # Найдём внешние круги
    n = len(circles)
    if n == 0:
        return np.array([])
    outside = get_touch_outside(P,
                                circles)  # TODO: можно чуть быстрее, проверяя расстояние до каждой грани многоугольника.
    layers = np.full(n, INT_MAX).astype('int')
    layers[outside] = 1  # Положим слой всех внешних вершин равным 1.

    # grid[(x, y)] = {Индексы всех кругов в клетке сетки}
    # Ширина сетки - 2r, где r - радиус кругов.
    grid = dict()
    # cell[i] = (x, y) - ячейка, в которой находится i-ый круг.
    cell = [(0, 0)] * n
    a = 2 * circles[0].radius
    for i in range(n):
        left = int(np.floor(circles[i].center.x) // a)
        bottom = int(np.floor(circles[i].center.y) // a)  # Вычислим координаты ячейки, в которой расположен круг.

        key = (left, bottom)
        if key in grid.keys():
            grid[key].append(i)
        else:
            grid[key] = [i]
        cell[i] = key

    def get_neighbors(v):
        """
        Находит все круги, которые пересекаются с кругом с индексом v.

        :param v: Индекс круга.
        :return: Список индексов кругов, с которыми пересекается заданный круг.
        """
        key = cell[v]
        x,y = key
        neighbors = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                new_key = (x + dx, y + dy)
                if new_key not in grid.keys():  # В этой ячейке нет кругов.
                    continue

                for i in grid[new_key]:
                    if i == v:
                        continue

                    cv = np.array(circles[v].center.xy)
                    ci = np.array(circles[i].center.xy)  # Координаты центров кругов.
                    dist = np.linalg.norm(cv - ci)
                    if dist <= 2 * circles[v].radius:
                        neighbors.append(i)
        return neighbors

    # Запустим BFS от внешних кругов.
    q = Queue()
    for i in range(n):
        if outside[i]:
            q.put(i)

    while not q.empty():
        v = q.get()
        value = layers[v] + 1
        neighbors = get_neighbors(v)
        for e in neighbors:
            if layers[e] > value:  # TODO: возможная эвристика: обрубать проход алгоритма, если достигли 2
                q.put(e)
                layers[e] = value

    return layers


def get_touch_outside(P: Polygon, circles: list[Circle]) -> np.array:
    n = len(circles)
    outside = np.zeros(n).astype('int')

    for i in range(n):
        c = circles[i]
        outside_area = c.polygon.area - P.intersection(c.polygon).area
        if outside_area > EPS:
            outside[i] = 1

    return outside
import numpy as np

from Utils.Circle import Circle
from shapely import Polygon


class Branch():
    """
    Ветвь в методе ветвей и границ.
    Хранит одно из состояний, в которое перейдёт алгоритм.
    """

    def __init__(self,
                 polygon: Polygon,
                 circles: list[Circle],
                 fixed: np.array = None):
        self.metric = None  # Значение перспективности ветви.
        self.polygon = polygon
        self.circles = circles
        if fixed is None:
            self.fixed = [0] * len(circles)
        else:
            self.fixed = fixed

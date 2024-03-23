from abc import ABC, abstractmethod

from shapely import Polygon

from Algorithms.Algorithm import Algorithm
from Utils.Circle import Circle


class RedundantRemover(Algorithm):
    def __init__(self, P: Polygon, circles: list[Circle]):
        self.circles = None
        self.input_ = circles
        self.P = P

    def set_params(self):
        pass

    def get_result(self) -> list[Circle]:
        return self.circles

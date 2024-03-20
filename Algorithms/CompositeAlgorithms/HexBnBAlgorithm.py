from shapely import Polygon

from Algorithms.Algorithm import Algorithm
from Utils.Circle import Circle

# TODO: перенести сюда exp_bnb
class HexBnBAlgorithm(Algorithm):
    def __init__(self,
                 P: Polygon,
                 circles: list[Circle]):
        self.P = P
        self.circles = circles

    def set_params(self):
        pass

    def run_algorithm(self):
        pass

    def get_result(self) -> list[Circle]:
        pass

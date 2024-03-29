from abc import ABC, abstractmethod
from Utils.Circle import Circle


class Algorithm(ABC):
    """
    Абстрактный базовый класс для всех алгоритмов.
    """
    # TODO: нужно ли задать конструктор?
    @abstractmethod
    def set_params(self):
        pass

    @abstractmethod
    def run_algorithm(self):
        pass

    @abstractmethod
    def get_result(self) -> list[Circle]:
        pass

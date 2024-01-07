import numpy as np
from scipy.integrate import RK45
from shapely import Point

from Algorithms.NBodies.GravityFunctions import smooth_gravity_with_sign
from Utils.Circle import Circle
from Utils.misc_funcs import group_n


class RungeKuttaAlgorithm:
    def __init__(self, centers: list[Point], radius: float):
        self.radius = radius
        self.centers = centers
        self.fixed = np.zeros(len(centers))

    def set_params(self,
                   fixed: np.array = None,
                   G: float = 0.1,
                   STOP_RADIUS: float = None,
                   TIME_START: float = 0,
                   TIME_STEP: float = 0.5,
                   TIME_STOP: float = 50,
                   gravity: 'gravity function' = smooth_gravity_with_sign):
        if fixed is not None:
            self.fixed = fixed
        self.G = G

        if STOP_RADIUS is None:
            self.STOP_RADIUS = self.radius
        else:
            self.STOP_RADIUS = STOP_RADIUS

        self.TIME_START = TIME_START
        self.TIME_STEP = TIME_STEP
        self.TIME_STOP = TIME_STOP
        self.gravity = gravity

    def __gravity(self, t, y: np.array):
        """
        Вспомогательная функция для передачи в метод Рунге-Кутта.
        Вычисляет дискретную производную в точке y в момент времени t для каждого тела.
        :param t: Момент времени, для которого происходит вычисление.
        :param y: Записанные в строку координаты тел: [x0, y0, x1, y1, x2, y2, ... ]
        :return: Дискретную производную по каждой переменной: [dx0, dy0, dx1, dy1, dx2, dy2, ... ]
        """
        n = y.shape[0]
        fn = np.zeros(n)
        # Считаем попарную силу взаимодействия с каждым другим телом.
        for i in np.arange(0, n, 2):
            if self.fixed[i // 2]:  # Если точка зафиксирована, оставим вектор для неё равным {0; 0}.
                continue

            A = np.array([y[i], y[i + 1]])
            for j in np.arange(0, n, 2):
                B = np.array([y[j], y[j + 1]])
                # Вычислим попарную силу взаимодействия всех точек с данной.
                # Функция гравитации должна для совпадающих точек возвращать 0.
                fn[i:i + 2] += smooth_gravity_with_sign(A,
                                                        B,
                                                        G=self.G,
                                                        STOP_RADIUS=self.STOP_RADIUS)
        return fn

    def run_algorithm(self):
        """
        centers = np.array([p.xy for p in self.centers]).flatten()

        t = self.TIME_START
        t_delta_max = self.TIME_STEP
        while t < self.TIME_STOP:
            delta = RK45(self.__gravity, t, centers, t + t_delta_max)
            t += t_delta_max
            centers += delta.f

        self.centers = [Point(p) for p in group_n(2, centers)]
        """

        centers = np.array([p.xy for p in self.centers]).flatten()
        t = self.TIME_START
        t_delta_max = self.TIME_STEP
        alg = RK45(self.__gravity, t, centers, self.TIME_STOP)
        while alg.t < self.TIME_STOP:
            alg.step() # Настроить параметр, чтобы не считалось так дотошно по 0.05 - мне так мелко не надо

        centers = alg.y  # Прибавим значение дискретной производной.
        self.centers = [Point(p) for p in group_n(2, centers)]


    def get_result(self):
        return [Circle(Point(c), self.radius) for c in self.centers]

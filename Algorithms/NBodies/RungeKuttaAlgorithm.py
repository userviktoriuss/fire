import numpy as np
from scipy.integrate import RK45
from shapely import Point

from Algorithms.NBodies.GravityFunctions import smooth_gravity_with_sign
from Algorithms.NBodies.Loggers import RKAnimationLogger
from Utils.Circle import Circle
from Utils.misc_funcs import group_n


class RungeKuttaAlgorithm:
    def __init__(self, centers: list[Point], radius: float):
        self.radius = radius
        self.centers = centers
        self.fixed = np.zeros(len(centers))

    def set_params(self,
                   fixed: np.array = None,  # По умолчанию все точки подвижны.
                   G: float = 0.1,
                   STOP_RADIUS: float = None,
                   TIME_START: float = 0,
                   TIME_STOP: float = 50,
                   RTOL: float = 0.000001,
                   ATOL: float = 0.005,  # При таких ATOL и RTOL ошибка будет в +- пол сантиметра
                   gravity: 'gravity function' = smooth_gravity_with_sign,
                   logger: RKAnimationLogger = None):
        if fixed is not None:
            self.fixed = fixed
        self.G = G

        if STOP_RADIUS is None:
            self.STOP_RADIUS = self.radius
        else:
            self.STOP_RADIUS = STOP_RADIUS

        self.TIME_START = TIME_START
        self.TIME_STOP = TIME_STOP
        self.RTOL = RTOL
        self.ATOL = ATOL
        self.gravity = gravity

        self.logger = logger

    def _gravity(self, t, y: np.array):
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
                fn[i:i + 2] += self.gravity(A,
                                            B,
                                            G=self.G,
                                            STOP_RADIUS=self.STOP_RADIUS)  # TODO: унифицировать все гравитации и добавить им в шаблонную сигнатуру время.
        return fn

    def run_algorithm(self):
        centers = np.array([p.xy for p in self.centers]).flatten()
        t = self.TIME_START
        alg = RK45(self._gravity, t, centers, self.TIME_STOP, rtol=self.RTOL, atol=self.ATOL)
        while alg.status == 'running':
            alg.step()
            if self.logger is not None:
                cords = alg.y.reshape(alg.y.size // 2, 2).T
                x = cords[0]
                y = cords[1]
                circles = [
                    Circle(Point(x[i], y[i]), self.radius)
                    for i in np.arange(x.size)
                ]

                self.logger.snap(circles)

        centers = alg.y  # Прибавим значение дискретной производной.
        self.centers = [Point(p) for p in group_n(2, centers)]

    def get_result(self):  # TODO: Может ему не надо строить прямо-таки круги?
        return [Circle(Point(c), self.radius) for c in self.centers]

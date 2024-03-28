import numpy as np
from shapely import Point, Polygon
from Algorithms.NBodies.GravityFunctions import smooth_gravity_with_sign
from Algorithms.NBodies.Loggers import RKAnimationLogger
from Algorithms.NBodies.PolyGravityFunctions import side_gravity
from Algorithms.NBodies.RungeKuttaAlgorithm import RungeKuttaAlgorithm


# По сути, тот же РК, что и RungeKuttaAlgorithm, но этот учитывает
# параметры многоугольника.
class RungeKuttaWithPolygonAlgorithm(RungeKuttaAlgorithm):
    def __init__(self, P: Polygon, centers: list[Point], radius: float):
        super().__init__(centers, radius)
        self.P = P

    def set_params(self,
                   fixed: np.array = None,  # По умолчанию все точки подвижны.
                   G: float = 0.2,
                   poly_G_out: float = 10,
                   poly_G_in: float = 0.3,
                   STOP_RADIUS: float = None,
                   TIME_START: float = 0,
                   TIME_STOP: float = 50,
                   RTOL: float = 0.000001,
                   ATOL: float = 0.005,  # При таких ATOL и RTOL ошибка будет в +- пол сантиметра
                   gravity: 'gravity function' = smooth_gravity_with_sign,
                   poly_gravity: 'gravity function with polygon' = side_gravity,
                   logger: RKAnimationLogger = None):  # TODO: гравитация!!!
        super().set_params(
            fixed,
            G,
            STOP_RADIUS,
            TIME_START,
            TIME_STOP,
            RTOL,
            ATOL,
            gravity,
            logger)
        self.poly_G_in = poly_G_in
        self.poly_G_out = poly_G_out
        self.poly_gravity = poly_gravity

    def _gravity(self, t, y: np.array):
        """
        Вспомогательная функция для передачи в метод Рунге-Кутта.
        Вычисляет дискретную производную в точке y в момент времени t для каждого тела.
        :param t: Момент времени, для которого происходит вычисление.
        :param y: Записанные в строку координаты тел: [x0, y0, x1, y1, x2, y2, ... ]
        :return: Дискретную производную по каждой переменной: [dx0, dy0, dx1, dy1, dx2, dy2, ... ]
        """
        n = y.shape[0]
        fn = super()._gravity(t, y)
        # Считаем попарную силу взаимодействия с каждым другим телом.
        for i in np.arange(0, n, 2):
            if self.fixed[i // 2]:  # Если точка зафиксирована, оставим вектор для неё равным {0; 0}.
                continue

            A = np.array([y[i], y[i + 1]])
            fn[i:i + 2] += self.poly_gravity(Point(A),
                                             self.P,
                                             G_in=self.poly_G_in,
                                             G_out=self.poly_G_out,
                                             STOP_RADIUS=self.STOP_RADIUS)

        return fn

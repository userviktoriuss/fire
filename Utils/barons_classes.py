import math
import random

from Utils.geometry import Point, Vector


class Resource:
    def __init__(self, A):
        self.A = A  # Точка.
        self.reset()

    def reset(self, timer=0):
        self.owners = 0
        self.timer = timer


class Baron:
    def __init__(self, C, r):
        self.C = C  # Точка.
        self.r = r
        self.reset()

    def reset(self, wealth=0, owns=0):
        self.wealth = wealth  # Богатство барона
        self.owns = owns  # Количество подвластных точек

    def is_owner_of(self, res):
        """
        Проверяет, что барон владеет точкой ресурсов.
        :param res: Точка ресурсов.
        :return: True/False - барон владеет/не владеет переданной точкой ресурсов.
        """
        return Vector(res.A, self.C).length() <= self.r

    def move(self, vector):
        """
        Сдвигает барона в сторону наибольшего дохода на distance.
        :param vector: Вектор перемещения.
        """
        self.C += vector


class Market:
    """
    Содержит всех баронов и все точки. Отвечает
     за всю систему в целом
    """

    def __init__(self, P, baron_count, r, net_resolution):
        """
        Создаёт рынок
        :param P: Многоугольник.
        :param baron_count:  Количество баронов.
        :param net_resolution: Разрешение сети - расстояние между соседними точками.
        """
        self.timer = 0
        self.P = P
        self.net = self.create_net(net_resolution)
        self.barons = self.create_barons(baron_count, r)

    def create_net(self, net_resolution):
        if net_resolution <= 0:
            return []

        net = []
        xs = [p.x for p in self.P.vertexes]
        ys = [p.y for p in self.P.vertexes]
        left = min(xs)
        right = max(xs)
        down = min(ys)
        up = max(ys)
        x = left

        while x <= right:
            y = down
            while y <= up:
                pnt = Point(x, y)
                if self.P.point_inside(pnt):
                    net.append(Resource(pnt))
                y += net_resolution
            x += net_resolution
        return net

    def create_barons(self, baron_count, r):
        barons = []
        xs = [p.x for p in self.P.vertexes]
        ys = [p.y for p in self.P.vertexes]
        left = min(xs)
        right = max(xs)
        down = min(ys)
        up = max(ys)

        for i in range(baron_count):
            x = random.uniform(left, right)
            y = random.uniform(down, up)
            baron = Baron(Point(x, y), r)
            barons.append(baron)

        return barons

    def update_ownership(self):  # TODO: как-то умнее и быстрее
        """
        Пересчитывает для каждой точки, сколько баронов ей владеет.
        Пересчитывает для баронов средний доход.
        """
        for point in self.net:
            point.owners = 0

        for baron in self.barons:
            baron.reset()
            for point in self.net:
                if baron.is_owner_of(point):
                    point.owners += 1
                    baron.owns += 1
                    baron.wealth += self.timer - point.timer  # TODO: надо ли добавить вес?
                    point.reset(self.timer)

    def next_iteration(self, step):
        """
        Производит следующую итерацию рынка: пересчитывает владения,
        двигает баронов, обновляет таймер

        :param step: Шаг обучения.
        """
        self.timer += 1  # Или в конце?
        self.update_ownership()
        changes = []
        # Векторы, которые показывают, как сдвинуться баронам
        # в сторону увеличения прибыли.
        # -Вычисление-: посчитаем средний уровень прибыли для барона.
        # Далее найдём среднее взвешенное всех подвластных точек
        # ресурсов: (отклонение от среднего) * (точка - центр).
        # -Искомый вектор-: (-step) * (средний взвешенный вектор).

        for baron in self.barons:
            if baron.owns == 0:
                changes.append(step * (baron.r / 2) * Vector(Point(0, 0), Point(math.sqrt(2) / 2, math.sqrt(2) / 2)))
                continue  # TODO: что делать здесь?

            v = Vector(Point(0, 0), Point(0, 0))
            avg = baron.wealth / baron.owns
            for point in self.net:
                if baron.is_owner_of(point):
                    v = v - Vector(baron.C, point.A)
            v = (step / baron.owns) * v
            changes.append(v)

        for i in range(len(changes)):
            self.barons[i].move(changes[i])

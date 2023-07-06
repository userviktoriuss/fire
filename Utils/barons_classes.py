import random

from Utils.geometry import Point


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

    def get_wealth(self):
        """
        :return: Считает уровень богатства барона
        """
        pass

    def move(self, distance):
        """
        Сдвигает барона в сторону наибольшего дохода на distance.
        :param distance: Величина перемещения.
        """
        pass


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
        xs = map(lambda p: p.x, self.P.vertexes)
        ys = map(lambda p: p.y, self.P.vertexes)
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
        xs = map(lambda p: p.x, self.P.vertexes)
        ys = map(lambda p: p.y, self.P.vertexes)
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

    def update_ownership(self):
        """
        Пересчитывает для каждой точки, сколько баронов ей владеет.
        """
        pass

    def next_iteration(self):
        """
        Производит следующую итерацию рынка: пересчитывает владения,
        двигает баронов, обновляет таймер
        """
        pass

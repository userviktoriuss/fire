class Resource:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.timer = 0
        self.owners = 0

    def reset(self, timer=0):
        self.owners = 0
        self.timer = timer


class Baron:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
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

    def __init__(self, P, baron_count, net_resolution):
        """
        Создаёт рынок
        :param P: Многоугольник.
        :param baron_count:  Количество баронов.
        :param net_resolution: Разрешение сети - расстояние между соседними точками.
        """
        self.timer = 0
        self.P = P
        self.net = self.create_net(net_resolution)
        self.barons = self.create_barons(baron_count)
        # создаём baron_count баронов
        raise Exception("not implemented")

    def create_net(self, net_resolution):
        net = []
        left = min(map(lambda p: p.x, self.P.vertexes))
        right = max(map(lambda p: p.x, self.P.vertexes))
        down = min(map(lambda p: p.y, self.P.vertexes))
        up = max(map(lambda p: p.y, self.P.vertexes))

    def update_ownership(self):
        """
        Пересчитывает для каждой точки, сколько баронов ей владеет
        """
        pass

    def next_iteration(self):
        """
        Производит следующую итерацию рынка: пересчитывает владения,
        двигает баронов, обновляет таймер
        """
        pass

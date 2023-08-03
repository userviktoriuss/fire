import random

from Utils.geometry import Polygon, Point, Vector, norm


class Particle:
    """
    Описывает частицу.
    """

    def __init__(self, A: Point, charge: float, mass: float):
        self.A = A  # Точка.
        self.charge = charge * (1 + random.random())
        self.mass = mass * (1 + random.random())
        self.velocity = Vector.zeros()


# deprecated
class BorderField:
    def __init__(self, P: Polygon,
                 k: float,
                 rigidity: float,
                 n_prtcls: int,
                 prtcl_charge: float,
                 prtcl_mass: float):
        self.P = P
        self.k = k  # Константа - характеристика поля.
        self.rigidity = rigidity  # Упругость - на сколько умножается скорость при столкновении со стенкой.

        xs = [p.x for p in self.P.vertexes]
        ys = [p.y for p in self.P.vertexes]
        self.left = min(xs)
        self.right = max(xs)
        self.down = min(ys)
        self.up = max(ys)

        self.particles = self.create_particles(n_prtcls, prtcl_charge, prtcl_mass)

    def get_point_inside(self, def_x, def_y):
        x = def_x
        y = def_y
        while not self.P.point_inside(Point(x, y)):  # TODO: Трэш реально.
            x = random.uniform(self.left, self.right)
            y = random.uniform(self.down, self.up)
        return Point(x, y)

    def create_particles(self,
                         n_prtcls: int,
                         prtcl_charge: float,
                         prtcl_mass: float) -> list[Particle]:
        """
        Заполняет поле частицами с заданными зарядом и массой.

        :param n_prtcls: Количество частиц.
        :param prtcl_charge: Заряд частиц.
        :param prtcl_mass: Масса частиц.
        :return: Массив созданных частиц.
        """
        particles = []

        for i in range(n_prtcls):
            ins = self.get_point_inside(self.left - 1, self.down - 1)
            prtcl = Particle(ins, prtcl_charge, prtcl_mass)
            particles.append(prtcl)

        return particles

    def time_iteration(self, time: float):
        """
        Обновляет состояние системы на time секунд вперёд, считая,
        что изменение сил взаимодействия за это время пренебрежимо мало.

        :param time: Время, на которое обновится система.
        :return:
        """

        # Пересчитаем скорости с помощью силы взаимодействия
        # между частицами.
        for i in range(len(self.particles)):
            for j in range(i + 1, len(self.particles)):
                p1 = self.particles[i]
                p2 = self.particles[j]
                v12 = Vector(p1.A, p2.A)
                r = v12.length()
                f = self.k * p1.charge * p2.charge / (r ** 2)
                a1 = -(f / p1.mass) * norm(v12)  # a = F/m.
                a2 = (f / p2.mass) * norm(v12)

                p1.velocity += + time * a1
                p2.velocity += time * a2

        # Проверим на столкновение со стенкой
        for p in self.particles:
            B = p.A + time * p.velocity

            if not self.P.point_inside(B):
                p.velocity = -self.rigidity * p.velocity  # TODO: зафиксить костыль
                # TODO: а может это фича, потому что это экономия n операций
                # а точки всё равно взаимодействуют

        # Подвинем частички
        for i, p in enumerate(self.particles):
            self.particles[i].A = p.A + time * p.velocity
            # TODO: убрать костыль
            if not self.P.point_inside(self.particles[i].A):
                self.particles[i].A = self.get_point_inside(self.left - 1, self.down - 1)
                self.particles[i].velocity = Vector.zeros()

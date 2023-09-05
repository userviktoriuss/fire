from shapely import Point, Polygon
import math


class Circle():
    def __init__(self,
                 center: Point,
                 radius: float,
                 circle_resolution: int = 100):
        self.center = center
        self.radius = radius

        points = []
        for i in range(circle_resolution):
            theta = 2 * math.pi * i / circle_resolution
            x = center.x + radius * math.cos(theta)
            y = center.y + radius * math.sin(theta)
            points.append(Point(x, y))

        self.polygon = Polygon(points)
        self.area = self.polygon.area

    @property
    def exterior(self):
        """
        Возвращает внешнюю границу круга.
        :return: Многоугольник, приближающий внешнюю границу круга.
        """
        return self.polygon.exterior

from Utils.Circle import Circle
from shapely import Point

class Baron(Circle):
    def move(self, dx, dy):
        new_c = Point(self.center.x + dx, self.center.y + dy)
        self.__init__(new_c, self.radius)
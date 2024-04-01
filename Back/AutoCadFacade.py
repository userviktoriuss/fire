import numpy as np
import pyautocad
from pyautocad import APoint
from shapely import Polygon, Point

from Back.ComWrapper import ComWrapper
from Utils.Circle import Circle
from Utils.misc_funcs import group_n


def make_polygon_from_polyline(coords: tuple[float]) -> Polygon:
    """
    По набору (x0, y0, x1, y1, x2, y2, ...) строит многоугольник.

    Заметим, что первая и последняя точки в наборе должны совпадать (x0 = xn, y0 = yn)

    :param coords: Набор координат, записанных подряд, вида (x0, y0, x1, y1, x2, y2, ...).
    :return: Многоугольник.
    """
    return Polygon([Point(np.round(p[0], 3), np.round(p[1], 3)) for p in group_n(2, coords)])


def make_points_from_polyline(coords: tuple[float]) -> list[Point]:
    """
    Разворачивает набор (x0, y0, x1, y1, x2, y2, ...) в список точек.

    :param coords: Набор координат, записанных подряд, вида (x0, y0, x1, y1, x2, y2, ...).
    :return: Список точек.
    """
    return [Point(np.round(p[0], 3), np.round(p[1], 3)) for p in group_n(2, coords)]


class AutoCadFacade():
    """
    Реализует паттерн Фасад для взаимодействия с
    приложением AutoCAD.
    """

    def __init__(self):
        self.acad = pyautocad.Autocad()

    def connect(self) -> str:
        """
        Проверяет доступ к запущенному приложению AutoCAD.
        Получает имя открытого чертежа.

        :return: Имя открытого чертежа.
        """
        doc = ComWrapper(self.acad.doc)
        return doc.Name

    def get_polygons(self) -> Polygon:
        """
        Получает выделенный многоугольник из приложения AutoCAD.

        Автоматически преобразовывает круги в многоугольники.

        Если выделено несколько многоугольников, считает первый
        из них внутренней границей, а последующие - полостями
        в первом.

        :return: Многоугольник, возможно содержащий полости.
        """
        selection = ComWrapper(self.acad.get_selection(text='Выберите полилинии:'))

        polygons = []
        for i in range(selection.Count):
            s = selection.Item(i)

            if s.EntityName == 'AcDbCircle':
                polygons.append(Circle(Point(s.center[0], s.center[1]), s.radius).polygon.exterior)

            if s.EntityName == 'AcDbPolyline':
                polygons.append(make_points_from_polyline(s.Coordinates))

        polygons.sort(reverse=True, key=lambda p: Polygon(p).area)
        return Polygon(polygons[0], polygons[1:])

    def draw_circles(self, circles: list[Circle]):
        """
        Отрисовывает круги в приложении AutoCAD.

        :param circles: Круги, которые нужно отрисовать.
        """
        model = ComWrapper(self.acad.model)
        for circle in circles:
            center = APoint(circle.center.x, circle.center.y)
            model.AddCircle(center, circle.radius)

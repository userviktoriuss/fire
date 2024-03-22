import numpy as np
import pyautocad
from pyautocad import APoint
from shapely import Polygon, Point

from Back.ComWrapper import ComWrapper
from Utils.Circle import Circle
from Utils.misc_funcs import group_n


# TODO: may be unused
def make_polygon_from_polyline(coords: tuple[float]) -> Polygon:
    return Polygon([Point(np.round(p[0], 3), np.round(p[1], 3)) for p in group_n(2, coords)])

def make_points_from_polyline(coords: tuple[float]) -> list[Point]:
    return [Point(np.round(p[0], 3), np.round(p[1], 3)) for p in group_n(2, coords)]


class AutoCadFacade():
    # TODO: всё проверить, на всё навесить try catch,
    # TODO: возвращать статусы / кидать ошибки так, чтобы по ним можно было строить мессадж боксы

    def __init__(self):
        self.acad = pyautocad.Autocad()

    def connect(self) -> str:
        doc = ComWrapper(self.acad.doc)
        return doc.Name

    def get_polygons(self) -> Polygon:
        selection = ComWrapper(self.acad.get_selection(text='Выберите полилинии:'))

        polygons = []
        for i in range(selection.Count):
            s = selection.Item(i)

            if s.EntityName == 'AcDbPolyline':
                polygons.append(make_points_from_polyline(s.Coordinates))
                # TODO: Добавить каст кругов autocad к моим.

        return Polygon(polygons[0], polygons[1:])

    def draw_circles(self, circles: list[Circle]):
        model = ComWrapper(self.acad.model)
        for circle in circles:
            center = APoint(circle.center.x, circle.center.y)
            model.AddCircle(center, circle.radius)

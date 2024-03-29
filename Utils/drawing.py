from matplotlib import pyplot as plt
from shapely import Polygon

# В этом файле заданы функции, используемые при тестировании
# для отрисовки кругов и многоугольников средствами
# библиотеки matplotlib.

# TODO: комментарии и типы

def draw_circle(axes, circle, color='turquoise', center_color='drakblue') -> None:
    drawing = plt.Circle((circle.center.x, circle.center.y), circle.radius, color=color, clip_on=False)
    axes.add_patch(drawing)
    axes.scatter([circle.center.x], [circle.center.y], color=center_color)


def draw_circles(axes, circles, color='turquoise', center_color='darkblue') -> None:
    for c in circles:
        drawing = plt.Circle((c.center.x, c.center.y), c.radius, color=color, clip_on=False)
        axes.add_patch(drawing)
    for c in circles:
        axes.scatter([c.center.x], [c.center.y], color=center_color)


# TODO: Добавить цвета
def draw_polygon(axes, P: Polygon) -> None:
    """
    Отрисовывает многоугольник с полостями в заданных осях.

    :param axes: Оси.
    :param P: Многоугольник.
    """
    axes.plot(P.exterior.xy[0], P.exterior.xy[1])
    for p_int in P.interiors:
        xx = [c[0] for c in p_int.coords]
        yy = [c[1] for c in p_int.coords]
        axes.plot(xx, yy, color='tab:blue')

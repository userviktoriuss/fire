from celluloid import Camera
from matplotlib import pyplot as plt
from shapely import Polygon

from Utils import Circle
from Utils.drawing import draw_polygon, draw_circles


class RKAnimationLogger:
    """
    Сохраняет промежуточные состояния работы метода Рунге-Кутты и строит по ним анимацию.
    """

    def __init__(self, P: Polygon):
        self.P = P

    def reset(self, xlim=(-6, 6), ylim=(-6, 6)):
        """
        Приводит логгер в готовое состояние.

        :param xlim: Ограничения для абсциссы графика.
        :param ylim: Ограничения для ординаты графика.
        """
        self.fig = plt.figure()
        self.ax = plt.axes(xlim=xlim, ylim=ylim)
        self.ax.set_aspect('equal', adjustable='box')
        self.camera = Camera(self.fig)

    def snap(self, circles: list[Circle]):
        """
        Делает снимок и добавляет его к анимации.
        """
        draw_polygon(self.ax, self.P)
        draw_circles(self.ax, circles)
        self.camera.snap()

    def save_log(self, path='rk_log.gif'):
        """
        Сохраняет собранную на данный момент анимацию.
        """
        animation = self.camera.animate()
        animation.save(path, writer='imagemagick')
        plt.close(self.fig)

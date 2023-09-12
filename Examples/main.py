from Algorithms.Baron.BaronsAlgorithm import Market
from Utils.geometry import *
from Algorithms.hexagonal import hexagonal
import matplotlib.pyplot as plt
import math
import random

# TODO: подогнать все методы под единый интерфейс (наверное, с учётом autocad)
from Utils.physical_classes import BorderField


def hexagonal_main():
    vertexes = [Point(20, 0),
                Point(0, 20),
                Point(20, 40),
                Point(40, 30),
                Point(30, 5)]
    P = Polygon(vertexes)

    plt.plot([20, 0, 20, 40, 30, 20], [0, 20, 40, 30, 5, 0])

    angle = math.pi / 6  # [0; pi/6]
    grid = hexagonal(P, 20, 20, 5, angle)
    plt.scatter([p.x for p in grid], [p.y for p in grid])
    plt.show()


def plot_market(fig, pause, market):
    fig.clear()

    xs = [p.x for p in market.P.vertexes]
    ys = [p.y for p in market.P.vertexes]
    plt.plot(xs + [xs[0]], ys + [ys[0]])

    free_points = list(filter(lambda p: p.owners == 0, market.net))
    xx = [p.A.x for p in free_points]
    yy = [p.A.y for p in free_points]
    plt.scatter(xx, yy)

    ax = fig.gca()
    for baron in market.barons:
        circle = plt.Circle((baron.C.x, baron.C.y), baron.r, color='green', clip_on=False)
        ax.add_patch(circle)

    plt.draw()
    plt.pause(pause)


def barons_main():
    vertexes = [Point(20, 0),
                Point(0, 20),
                Point(20, 40),
                Point(40, 30),
                Point(30, 5)]
    P = Polygon(vertexes)
    market = Market(P, 16, 5, 0.5)

    fig = plt.figure()
    plot_market(fig, 0.2, market)
    tau = 0.5  # Скорость "обучения"
    while tau > 1e-8:
        market.next_iteration(tau)
        plot_market(fig, 0.2, market)
        tau *= 0.99

    input("Press the Enter key to Exit.")


def plot_border_field(fig, pause, field: BorderField):
    fig.clear()

    xs = [p.x for p in field.P.vertexes]
    ys = [p.y for p in field.P.vertexes]
    plt.plot(xs + [xs[0]], ys + [ys[0]])

    ax = fig.gca()
    for p in field.particles:
        plt.scatter(p.A.x, p.A.y, color=random.choice('rgb'))

    plt.draw()
    plt.pause(pause)


def border_like_physical_main():
    vertexes = [Point(20, 0),
                Point(0, 20),
                Point(20, 40),
                Point(40, 30),
                Point(30, 5)]
    P = Polygon(vertexes)

    field = BorderField(P, 2, 0.9, 18, 10, 0.0005)

    step = 0.001
    for i in range(300):
        field.time_iteration(step)
        # step -= 0.0001
        # step *= 0.98

    xs = [p.x for p in field.P.vertexes]
    ys = [p.y for p in field.P.vertexes]
    plt.plot(xs + [xs[0]], ys + [ys[0]])
    for p in field.particles:
        plt.scatter(p.A.x, p.A.y, color=random.choice('rgb'))
    plt.show()

def some_weird_test():
    vertexes = [Point(20, 0),
                Point(0, 20),
                Point(20, 40),
                Point(40, 30),
                Point(30, 5)]
    P = Polygon(vertexes)
    bounding = Bounding.from_polygon(P)
    print(bounding)


if __name__ == '__main__':
    some_weird_test()

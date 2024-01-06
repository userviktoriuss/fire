import numpy as np
from celluloid import Camera
from matplotlib import pyplot as plt
from numpy.random import randint
from scipy.integrate import RK45
from GravityFunctions import smooth_gravity_with_sign
from Utils.misc_funcs import group_n


def __rk_sub(t, y: np.array):
    n = y.shape[0]
    fn = np.zeros(n)
    for i in range(0, n, 2):
        A = np.array([y[i], y[i + 1]])
        for j in range(0, n, 2):
            if i == j:
                continue
            B = np.array([y[j], y[j + 1]])
            tmp = smooth_gravity_with_sign(A, B, G=0.1)
            fn[i:i + 2] += tmp
    return fn


def RungeKutta(points, t_start, t_end):
    return RK45(__rk_sub, t_start, points, t_end)


if __name__ == '__main__':
    points = np.array([[randint(-5, 5), randint(-5, 5)] for i in range(10)]).astype('float')

    fig = plt.figure()
    ax = plt.axes(xlim=(-6, 6), ylim=(-6, 6))
    camera = Camera(fig)

    t = 0
    t_delta_max = 0.5
    for i in range(100):
        delta = RungeKutta(points.flatten(), t, t_delta_max)
        t = delta.t
        points += np.array(group_n(2, delta.f))
        ax.scatter(points[:, 0], points[:, 1])
        camera.snap()

    animation = camera.animate()
    animation.save('runge_kutta_points.gif', writer='imagemagick')

"""
if __name__ == '__main__':
    points = np.array([[randint(-5, 5), randint(-5, 5)] for i in range(10)]).astype('float')
    fig = plt.figure()
    ax = plt.axes(xlim=(-6, 6), ylim=(-6, 6))
    camera = Camera(fig)

    for i in range(200):
        ax.scatter(points[:, 0], points[:, 1])

        camera.snap()
        #points = Euler(points, 0.01, 0.01, smooth_gravity_with_sign) #cut_gravity_with_sign

    animation = camera.animate()
    animation.save('runge_kutta_points.gif', writer='imagemagick')
"""

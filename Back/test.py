from scipy.stats.qmc import Halton
import matplotlib.pyplot as plt

h = Halton(d=2)
x = h.random(100)
plt.scatter(x[:, 0].T, x[:, 1].T, c='black')
plt.xlim(0, 1)
plt.ylim(0, 1)
ax = plt.gca()
ax.set_aspect('equal', adjustable='box')
ax.set_facecolor((69/255, 79/255, 97/255))
plt.draw()
plt.show()
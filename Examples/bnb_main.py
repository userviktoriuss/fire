import math
import time

from matplotlib import pyplot as plt

# from Utils.geometry import Polygon, Point
# from Algorithms.hexagonal import hexagonal

from shapely import Point, Polygon, unary_union

from Algorithms.BranchesAndBounds.BranchesAndBounds import bnb
from Algorithms.Hexagonal.hexagonal import hexagonal
from Examples.polygons import polygons_dict
from Utils.Circle import Circle

EPS = 1e-3
RESOLUTION = 5
ALPHA_RESOLUTION = 5

def get_important(P_described, P, S, alpha):
    outer_grid = hexagonal(P_described, S, 1, alpha)

    inside = [Circle(c, 1) for c in outer_grid if P.contains(c)]
    outside = [Circle(c, 1) for c in outer_grid if not P.contains(c)]
    union = unary_union([c.polygon for c in inside])

    outside.sort(key=
                 lambda c: P.intersection(c.polygon).area,
                 reverse=True)
    for c in outside:
        c_inside_polygon = P.intersection(c.polygon)
        united = unary_union([union, c_inside_polygon])
        if abs(united.area - union.area) > EPS:
            inside.append(c)
            union = unary_union([union, c_inside_polygon])
    return [c.center for c in inside]


# Main part

P = polygons_dict['P8']
(minx, miny, maxx, maxy) = P.bounds
P_described = Polygon([Point(minx - 1, miny - 1), Point(maxx + 1, miny - 1), Point(maxx + 1, maxy + 1), Point(minx - 1, maxy + 1)])
inners = []

for inn in inners:
    P = P.difference(inn)

t0 = time.perf_counter()
best_ops = (0, 0, 0)
best_val = 1e20

step_alpha = math.pi / 3 / ALPHA_RESOLUTION
step_x = 1 / RESOLUTION
step_y = 1 / RESOLUTION
alpha = 0
while alpha < math.pi / 3:
    x = 0
    while x < 1:
        y = 0
        while y < 1:
            S = Point(x, y)

            important = get_important(P_described, P, S, alpha)

            if len(important) < best_val:
                best_val = len(important)
                best_ops = (x, y, alpha)
            y += step_y
        x += step_x
    alpha += step_alpha

t1 = time.perf_counter()
print(f'Elapsed time: {t1 - t0} sec.')
print(f'Best value is: {best_val} circles')
print(f'Best ops: ({best_ops[0]}; {best_ops[1]}), alpha={best_ops[2]}')
fig = plt.figure()
ax = fig.gca()
ax.set_aspect('equal', adjustable='box')

plt.plot(P.exterior.xy[0], P.exterior.xy[1])
for p_int in P.interiors:
    xx = [c[0] for c in p_int.coords]
    yy = [c[1] for c in p_int.coords]
    plt.plot(xx, yy, color='tab:blue')


best_grid = get_important(P_described, P, Point(best_ops[0], best_ops[1]), best_ops[2])
for p in best_grid:
    c = 'turquoise'
    circle = plt.Circle((p.x, p.y), 1, color=c, clip_on=False)
    ax.add_patch(circle)

plt.scatter([p.x for p in best_grid], [p.y for p in best_grid], color='darkblue')
plt.show()

# ------------------------------------
bnb_grid = bnb(P, best_grid, is_repaired=True)
print(f'BnB results: {len(bnb_grid)}.')

fig = plt.figure()
ax = fig.gca()
ax.set_aspect('equal', adjustable='box')

plt.plot(P.exterior.xy[0], P.exterior.xy[1])
for p_int in P.interiors:
    xx = [c[0] for c in p_int.coords]
    yy = [c[1] for c in p_int.coords]
    plt.plot(xx, yy, color='tab:blue')


for p in bnb_grid:
    c = 'turquoise'
    circle = plt.Circle((p.x, p.y), 1, color=c, clip_on=False)
    ax.add_patch(circle)

plt.scatter([p.x for p in bnb_grid], [p.y for p in bnb_grid], color='darkblue')
plt.show()

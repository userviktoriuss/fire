import comtypes

import pyautocad
from pyautocad import APoint
from shapely import Polygon, Point

from Algorithms.BranchesAndBounds.BranchesAndBounds import BnBAlgorithm
from Algorithms.Hexagonal.HexagonalAlgorithm import HexagonalAlgorithm
from Algorithms.NBodies.GravityFunctions import smooth_gravity_on_region_with_sign
from Algorithms.NBodies.RungeKuttaAlgorithm import RungeKuttaAlgorithm
from Back.ComWrapper import ComWrapper
from Utils.layering import get_layers
from Utils.misc_funcs import group_n
import numpy as np

acad = pyautocad.Autocad()

doc = ComWrapper(acad.doc)
# Если выбросится исключение, значит, документ занят и мы не сможем с ним работать.
print('Подключаемся к текущему документу...')
print(f'Успешно подключились к документу {doc.Name}.')

selection = ComWrapper(acad.get_selection(text='Выберите полилинии:'))

polygons = []
for i in range(selection.Count):
    s = selection.Item(i)

    if s.EntityName == 'AcDbPolyline':
        polygons.append(make_polygon_from_polyline(s.Coordinates))


# -------------------------------------------------------------------------
# попробуем построить покрытие и отобразить его
for p in polygons:
    print(p)

P = polygons[0]
R = 1.5  # Радиус.
INNER_BOUND = 2  # Начиная с этого слоя по удалению от внешних границ многоугольника круг считается внутренним.

# Построим покрытие шестиугольной сеткой.
hex_alg = HexagonalAlgorithm(P, R)  # Укажем данные.
hex_alg.set_params()  # Укажем параметры решения.
hex_alg.run_algorithm()  # Запустим алгоритм.
hex_ans = hex_alg.get_result()  # Получим результат - list[Circle].

# Разложим круги по уровням дальности до края многоугольника
layers = get_layers(P, hex_ans)

# Выделим "внутренние" круги.
inners = np.zeros(len(layers))
inners[layers >= INNER_BOUND] = 1

# Починим методом ветвей и границ
bnb_alg = BnBAlgorithm(P, hex_ans)
bnb_alg.set_params(
    max_iterations=15,
    fixed=list(inners),
    ALPHA = 0,  # Влияние самопересечений.
    BETA = 0.05,  # Влияние отношения покрытой площади вне многоугольника к площади многоугольника.
    GAMMA = 0.005,  # Влияние количества кругов по отношению к стартовому.
    LAMBDA = 1.5,  # Влияние процента покрытия.
    DELETE_PROB=1
)
bnb_alg.run_algorithm()
bnb_grid = bnb_alg.get_result()

# Придвинем поближе внешние круги с помощью метода Рунге-Кутта.
rk_alg = RungeKuttaAlgorithm(
    [c.center for c in bnb_grid],
    R)
rk_alg.set_params(
    fixed=bnb_alg.fixed,  # TODO: другие параметры???,
    STOP_RADIUS=1.5 * R,
    TIME_STOP=20,
    gravity=smooth_gravity_on_region_with_sign
)
rk_alg.run_algorithm()
rk_ans = rk_alg.get_result()


model = ComWrapper(acad.model)
for circle in rk_ans:
    center = APoint(circle.center.x, circle.center.y)
    model.AddCircle(center, circle.radius)
print('Успешно завершено!')
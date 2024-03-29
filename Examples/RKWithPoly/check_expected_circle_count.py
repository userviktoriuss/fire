import numpy as np

from Examples.polygons import polygons_dict
from Utils.circle_count import expected_circle_count, expected_circle_count2

for e in polygons_dict:
    P = polygons_dict[e]
    R = 1.5
    k1 = expected_circle_count(P, R)  # Ожидаемое количество кругов, необходимое для покрытия.
    k2 = expected_circle_count2(P, R)
    k_weighted = int(np.ceil((k1 * 4 + k2) / 5))
    print(f'{e}: {k1}, {k2}, {k_weighted}')

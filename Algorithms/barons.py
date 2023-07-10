from Utils.barons_classes import Market


# Заполняет многоугольник кругами по методу "Баронов"

def barons(P,
           init_tau, change_tau, end_tau,  # TODO: класс schedule
           baron_count, baron_r,
           net_resolution):
    """
    Заполняет многоугольник кругами по методу "Баронов".

    :param P: Многоугольник.
    :param init_tau: Начальное значение скорости изменения среды.
    :param change_tau: Мультипликатор скорости изменения среды.
    :param end_tau: Нижнее значение скорости изменения среды.
    :param baron_count: Количество баронов.
    :param baron_r: Радиус влияния барона.
    :param net_resolution: Расстояние между соседними точками сетки.
    :return: Центры кругов для замощения многоугольника.
    """
    market = Market(P, baron_count, baron_r, net_resolution)

    tau = 0.5  # Скорость "обучения"
    while tau > 1e-8:
        market.next_iteration(tau)
        tau *= 0.99

    return [baron.C for baron in market.barons]

import numpy as np

from Algorithms.BranchesAndBounds.FlexibleBnBAlgorithm import FlexibleBnBAlgorithm
from Algorithms.BranchesAndBounds.ParamsClasses.StretchedBnBParams import StretchedBnBParams
from Algorithms.NBodies.GravityFunctions import repel_cut_gravity
from Algorithms.NBodies.PolyGravityFunctions import side_gravity
from Algorithms.NBodies.RundeKuttaWithPolygonAlgorithm import RungeKuttaWithPolygonAlgorithm
from Front.Fonts import Fonts
from Front.UiClasses.AlgorithmFrame import AlgorithmFrame, TextInfo
import customtkinter as ctk

from Front.UiClasses.MsgBox import MsgBox
from Utils.misc_funcs import expected_circle_count, expected_circle_count2, expected_circle_count_weighted, \
    point_inside_polygon


class RkGeneticAlgorithmFrame(AlgorithmFrame):
    '''
    Класс для страницы покрытия методом Шестиугольной сетки.

    Определяет описание алгоритма, поля заполнения параметров и
    вызов алгоритма с заданными параметрами.
    '''
    title = 'Гравитационный алгоритм'
    text_info = TextInfo(
        description=
        '''Этот метод пытается оптимизировать покрытие, полученное уравновешиванием системы отталкивающихся друг от друга и от границ многоугольника тел. Изначально круги генерируются случайно внутри многоугольника. Затем моделируется поведение системы в заданном промежутке времени, после чего происходит корректировка покрытия с помощью генетического алгоритма.
        ''',
        params=
        '''Гравитационный алгоритм.
· R - радиус кругов, которыми покрывается многоугольник.
· EXPECTED_CITCLE_COUNT: алгоритм выбирает, какое количество кругов изначально сгенерировать по одной из стратегий:
- Для прямоугольного многоугольника - самая низкая из оценок. Лучше всего подойдёт для многоугольника, имеющего мало скруглений.
- Для круга - самая высокая из оценок. Лучше всего подойдёт для округлых фигур.
- Комбинированная - это копромиссная стратегия. Взвешивает предыдущие две оценки в соотношении 4:1.

· TIME_START - время, начиная с которого будем моделировать систему.
· TIME_STOP - время, до которого моделируем систему.

· GRAVITY - функция, показывающая степень взаимодействия двух тел. Используется для расчёта передвижения кругов. По сути, задаёт добавку к скорости в данной точке.
· G - константа для масштабирования GRAVITY
· POLY_GRAVITY - функция, показывающая степень взаимодействия тела и многоугольника. По сути, задаёт добавку к скорости в данной точке.
· G_IN_POLY - константа для масштабирования POLY_GRAVITY, если точка лежит внутри многоугольника.
· G_OUTSIDE_POLY - константа для масштабирования POLY_GRAVITY, если точка лежит вне многоугольника.
 
На больших расстояниях сила притяжения/отталкивания объектов принимается прямо/обратно пропорциональной квадрату расстояния.
· STOP_RADIUS - если два тела (тело и стена) находятся ближе этого расстояния друг от друга, то степень их взаимодействия начинает вычисляться по ограниченной формуле (обратно квадратичная формула даёт очень большой прирост скорости на маленьких расстояниях)

Генетический алгоритм.
· int(ITERATION_MULT * k) - максимальное количество итераций генетического алгоритма, где k - количество сгенерированных в начале алгоритма кругов.
· MOVE_SCHEDULER_MULT - какая доля от скорости перемещения кругов остаётся после каждой итерации (то есть, алгоритм должен более аккуратно двигать круги на поздних стадиях).
Создание особей:
· ANGLE_RESOLUTION - в скольких направления будут создаваться особи
· MOVE_MULTIPLIER - множитель расстояния, на которое может сдвинуться особь
Метрика, которую оптимизирует генетический алгоритм, состоит из четырёх параметров:
· SELF_INTER - важность попарного пересечения кругов (чем чаще круги накладываются друг на друга, тем меньше метрика)
· OUTSIDE - важность того, какая часть площади кругов лежит за границей многоугольника
· COVERAGE - важность того, какой процент многоугольника покрыт
· CIRCLE_COUNT - важность количества кругов (на этапе перемещения)
''',
        recommended_values=
        '''· EXPECTED_CIRCLE_COUNT = Комбинированная

· TIME_START - время, начиная с которого будем моделировать систему.
· TIME_STOP - время, до которого моделируем систему.

· GRAVITY = Ограниченное отталкивание.
· G = 0.2
· POLY_GRAVITY = Затягивающее внутрь.
· G_IN_POLY = 0.15
· G_OUTSIDE_POLY = 10
· STOP_RADIUS = R

· ITERATION_MULT = 1-1.1
· MOVE_SCHEDULER_MULT = 0.985

· ANGLE_RESOLUTION = 6
· MOVE_MULTIPLIER = 1.5
· SELF_INTER = 0
· OUTSIDE = 0.05
· COVERAGE = 1.5
· DEL_CIRCLE_COUNT = 0.1
· CIRCLE_COUNT = 0.005
''',
        notes=
        '''Это довольно результативный метод. На маленьких фигурах он справляется лучше остальных. Однако, он может требовать больше времени.
'''
    )

    circle_count_methods = {
        'Для прямоугольного многоугольника': expected_circle_count,
        'Для круга': expected_circle_count2,
        'Комбинированная': expected_circle_count_weighted
    }

    gravities = {
        'Ограниченное отталкивание': repel_cut_gravity,
    }

    poly_gravities = {
        'Затягивающее внутрь': side_gravity,
    }

    def fill_left_panel_(self):
        self.line1 = ctk.CTkFrame(self.left_panel)
        self.line23 = ctk.CTkFrame(self.left_panel)
        self.line2 = ctk.CTkFrame(self.line23)
        self.line3 = ctk.CTkFrame(self.line23)
        self.line4 = ctk.CTkFrame(self.left_panel)
        self.line5 = ctk.CTkFrame(self.left_panel)
        self.line6 = ctk.CTkFrame(self.left_panel)

        # line1 --------------------------------------------------------
        self.alg_label = ctk.CTkLabel(self.line1, text=self.title, font=Fonts.header_font)
        self.alg_label.pack(side='top')
        # line2 --------------------------------------------------------
        self.line2.columnconfigure(0, weight=1)
        self.line2.columnconfigure(1, weight=4)
        self.line2.rowconfigure((0, 1), weight=1)

        self.add_label_input_pair_('R', self.line2, row=0)
        self.add_label_combobox_pair_(
            'EXPECTED_CIRCLE_COUNT',
            self.line2,
            'EXPECTED_CIRCLE_COUNT',
            list(self.circle_count_methods.keys()),
            row=1
        )

        # line3 ---------------------------------------------------------
        self.line3.columnconfigure(0, weight=1)
        self.line3.columnconfigure(1, weight=4)
        self.line3.rowconfigure(tuple(range(2)), weight=1)

        self.add_label_input_pair_('TIME_START', self.line3, row=0, width=50)
        self.add_label_input_pair_('TIME_STOP', self.line3, row=1, width=50)

        # line4 -----------------------------------------------------------
        self.line4.columnconfigure(0, weight=1)
        self.line4.columnconfigure(1, weight=4)
        self.line4.rowconfigure(tuple(range(6)), weight=1)

        self.add_label_combobox_pair_(
            'GRAVITY',
            self.line4,
            'GRAVITY',
            list(self.gravities.keys()),
            row=0
        )
        self.add_label_input_pair_('G', self.line4, row=1)

        self.add_label_combobox_pair_(
            'POLY_GRAVITY',
            self.line4,
            'POLY_GRAVITY',
            list(self.poly_gravities.keys()),
            row=2
        )
        self.add_label_input_pair_('G_IN_POLY', self.line4, row=3)
        self.add_label_input_pair_('G_OUTSIDE_POLY', self.line4, row=4)
        self.add_label_input_pair_('STOP_RADIUS', self.line4, row=5)

        # line5 -----------------------------------------------------------
        self.line5.columnconfigure(0, weight=1)
        self.line5.rowconfigure((0, 1), weight=1)
        self.add_label_input_pair_('ITERATIONS_MULT', self.line5, row=0)
        self.add_label_input_pair_('MOVE_SCHEDULE_MULT', self.line5, row=1)

        # line6 -----------------------------------------------------------
        self.line6.columnconfigure(0, weight=1)
        self.line6.columnconfigure(1, weight=4)
        self.line6.rowconfigure(tuple(range(6)), weight=1)

        self.add_label_input_pair_('ANGLE_RESOLUTION', self.line6, row=0, type_=int)
        self.add_label_input_pair_('MOVE_MULTIPLIER', self.line6, row=1)
        self.add_label_input_pair_('SELF_INTER', self.line6, row=2)
        self.add_label_input_pair_('OUTSIDE', self.line6, row=3)
        self.add_label_input_pair_('COVERAGE', self.line6, row=4)
        self.add_label_input_pair_('CIRCLE_COUNT', self.line6, row=5)

        # grid ------------------------------------------------------------
        # Расположим все строки в левой части.
        self.line2.grid(row=0, column=0, stick='news', padx=5, pady=10)
        self.line3.grid(row=0, column=1, stick='news', padx=10, pady=10)

        self.line1.grid(row=0, column=0, stick='news', padx=20, pady=10)
        self.line23.grid(row=1, column=0, stick='news', padx=20, pady=10)
        self.line4.grid(row=2, column=0, stick='news', padx=20, pady=10)
        self.line5.grid(row=3, column=0, stick='news', padx=20, pady=10)
        self.line6.grid(row=4, column=0, stick='news', padx=20, pady=10)


    def run_alg_(self):
        # Получим многоугольник.
        try:
            poly = self.autocad.get_polygons()
        except:
            MsgBox.show_error_msgbox('Не удалось получить многоугольник(и). \nПрервите все активные команды и попробуйте снова.')
            return

        # Получим параметры алгоритма.
        try:
            R = self.get_('R')
            exp_circle_cnt_method = self.get_('EXPECTED_CIRCLE_COUNT')
            # ---
            time_start = self.get_('TIME_START')
            time_stop = self.get_('TIME_STOP')
            # ---
            gravity = self.get_('GRAVITY')
            g = self.get_('G')

            poly_gravity = self.get_('POLY_GRAVITY')
            g_in_poly = self.get_('G_IN_POLY')
            g_outside_poly = self.get_('G_OUTSIDE_POLY')
            stop_radius = self.get_('STOP_RADIUS')
            # ---
            iters_mult = self.get_('ITERATIONS_MULT')
            move_schedule_mult = self.get_('MOVE_SCHEDULE_MULT')
            # ---
            angle_res = self.get_('ANGLE_RESOLUTION')
            move_mult = self.get_('MOVE_MULTIPLIER')
            self_inter = self.get_('SELF_INTER')
            outside = self.get_('OUTSIDE')
            coverage = self.get_('COVERAGE')
            circle_count = self.get_('CIRCLE_COUNT')
        except:
            print('Parsing exception')  # TODO: кидать здесь и в других сообщение, а-то непонятно, что ничего не считается.
            return

        # Запустим алгоритм.
        expected_circles = self.circle_count_methods[exp_circle_cnt_method](poly, R)
        centers = [point_inside_polygon(poly) for _ in range(expected_circles)]


        alg = RungeKuttaWithPolygonAlgorithm(poly, centers, R)  # Укажем данные.
        alg.set_params(
            fixed=[0 for _ in range(expected_circles)],
            gravity=self.gravities[gravity],
            G=g,
            poly_gravity=self.poly_gravities[poly_gravity],
            poly_G_out=g_outside_poly,
            poly_G_in=g_in_poly,  # 0.2,  # 0.3
            STOP_RADIUS=stop_radius,
            TIME_START=time_start,
            TIME_STOP=time_stop
        )  # Укажем параметры решения.
        # Запуск алгоритма

        alg.run_algorithm()  # Запустим алгоритм.

        ans = alg.get_result()  # Получим результат - list[Circle].

        # logger.save_log(f'{name}_rk_log_{alg.G}_{alg.poly_G_out}_{alg.poly_G_in}.gif')


        bnb_alg = FlexibleBnBAlgorithm(poly, ans)

        bnb_alg.set_params(
            max_iterations=int(np.ceil(iters_mult * expected_circles)),
            params=StretchedBnBParams(
                P=poly,
                ANGLE_RESOLUTION=angle_res,
                MOVE_MULTIPLIER=move_mult,
                init_circles=expected_circles,
                SELF_INTER_W=self_inter,
                OUTSIDE_W=outside,
                COVERAGE_W=coverage,
                CIRCLE_COUNT_W=circle_count,
                MOVE_SCHEDULE=(lambda x: move_schedule_mult * x)),
        )
        bnb_alg.run_algorithm()
        circles = bnb_alg.get_result()

        # Вернём ответ.
        try:
            self.autocad.draw_circles(circles)
        except:
            MsgBox.show_error_msgbox('Не удалось отрисовать покрытие. \nПрервите все активные команды и попробуйте снова.')
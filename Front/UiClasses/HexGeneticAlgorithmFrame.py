import numpy as np

from Algorithms.BranchesAndBounds.FlexibleBnBAlgorithm import FlexibleBnBAlgorithm
from Algorithms.BranchesAndBounds.ParamsClasses.StretchedBnBParams import StretchedBnBParams
from Algorithms.Hexagonal.HexagonalAlgorithm import HexagonalAlgorithm
from Algorithms.Hexagonal.hexagonal_coverings import hexagonal_np
from Front.Fonts import Fonts
from Front.UiClasses.AlgorithmFrame import AlgorithmFrame, TextInfo
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from Front.UiClasses.MsgBox import MsgBox
from Utils.layering import get_layers


class HexGeneticAlgorithmFrame(AlgorithmFrame):
    '''
    Класс для страницы покрытия методом Шестиугольной сетки.

    Определяет описание алгоритма, поля заполнения параметров и
    вызов алгоритма с заданными параметрами.
    '''
    title = 'Генетический алгоритм'
    text_info = TextInfo(
        description=
        '''Этот метод пытается оптимизировать построенное методом шестиугольной сетки покрытие с помощью метрики. Метрика поощряет особь за большую площадь покрытия и наказывает за большое количество кругов, большое попарное их пересечение и выходы за пределы многоугольника.
        ''',
        params=
        '''· R - радиус кругов, которыми покрывается многоугольник.
· ALPHA_RESOLUTION - сколько разных углов от 0 до π/3 будет перебирать алгоритм.
· RESOLUTION - сколько сдвигов будет перебирать алгоритм.

Генетический алгоритм состоит из двух стадий: с приоритетом на удаление и перемещение кругов. В каждой стадии количество итераций пропорционально количеству кругов n. 
· int(ITERATION_MULT_DELETION * n) - количество итераций на стадии удаления кругов.
· int(ITERATION_MULT_MOVING * n) - количество итераций на стадии перемещения кругов.
Алгоритм затрагивает только "внешние" круги. 
· INNER BOUND - начиная с этого слоя по удалению от внешних границ многоугольника круг считается "внутренним".
· MOVE_SCHEDULER_MULT - какая доля от скорости перемещения кругов остаётся после каждой итерации (то есть, алгоритм должен более аккуратно двигать круги на поздних стадиях).
Создание особей:
· ANGLE_RESOLUTION - в скольких направления будут создаваться особи
· MOVE_MULTIPLIER - множитель расстояния, на которое может сдвинуться особь
Метрика, которую оптимизирует алгоритм, состоит из четырёх параметров:
· SELF_INTER - важность попарного пересечения кругов (чем чаще круги накладываются друг на друга, тем меньше метрика)
· OUTSIDE - важность того, какая часть площади кругов лежит за границей многоугольника
· COVERAGE - важность того, какой процент многоугольника покрыт
· DEL_CIRCLE_COUNT - важность количества кругов (на этапе удаления)
· CIRCLE_COUNT - важность количества кругов (на этапе перемещения)
''',
        recommended_values=
        '''· ALPHA_RESOLUTION, RESOLUTION не стоит брать большими, 1-3 вполне достаточно.
· ITERATION_MULT_DELETION = 0.3-0.4
· ITERATION_MULT_MOVING = 1-2

· INNER BOUND = 2
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
        '''Это довольно результативный метод. Однако, он может требовать больше времени, чем другие.
'''
    )

    def fill_left_panel_(self):
        self.line1 = ctk.CTkFrame(self.left_panel)
        self.line2 = ctk.CTkFrame(self.left_panel)
        self.line3 = ctk.CTkFrame(self.left_panel)
        self.line4 = ctk.CTkFrame(self.left_panel)

        # line1 --------------------------------------------------------
        self.alg_label = ctk.CTkLabel(self.line1, text=self.title, font=Fonts.header_font)
        self.alg_label.pack(side='top')
        # line2 --------------------------------------------------------
        self.line2.columnconfigure(0, weight=1)
        self.line2.columnconfigure(1, weight=4)
        self.line2.rowconfigure((0, 1, 2), weight=1)

        self.add_label_input_pair_('R', self.line2, row=0)
        self.add_label_input_pair_('ALPHA_RESOLUTION', self.line2, row=1, type_=int)
        self.add_label_input_pair_('RESOLUTION', self.line2, row=2, type_=int)

        # line3 ---------------------------------------------------------
        self.line3.columnconfigure(0, weight=1)
        self.line3.columnconfigure(1, weight=4)
        self.line3.rowconfigure(tuple(range(4)), weight=1)

        self.add_label_input_pair_('ITERATIONS_MULT_DELETION', self.line3, row=0)
        self.add_label_input_pair_('ITERATIONS_MULT_MOVING', self.line3, row=1)
        self.add_label_input_pair_('INNER_BOUND', self.line3, row=2, type_=int)
        self.add_label_input_pair_('MOVE_SCHEDULE_MULT', self.line3, row=3)

        # line4 -----------------------------------------------------------
        self.line4.columnconfigure(0, weight=1)
        self.line4.columnconfigure(1, weight=4)
        self.line4.rowconfigure(tuple(range(7)), weight=1)

        self.add_label_input_pair_('ANGLE_RESOLUTION', self.line4, row=0, type_=int)
        self.add_label_input_pair_('MOVE_MULTIPLIER', self.line4, row=1)
        self.add_label_input_pair_('SELF_INTER', self.line4, row=2)
        self.add_label_input_pair_('OUTSIDE', self.line4, row=3)
        self.add_label_input_pair_('COVERAGE', self.line4, row=4)
        self.add_label_input_pair_('DEL_CIRCLE_COUNT', self.line4, row=5)
        self.add_label_input_pair_('CIRCLE_COUNT', self.line4, row=6)

        # grid ------------------------------------------------------------
        # Расположим все строки в левой части.
        self.left_part_frame.columnconfigure(0, weight=1)
        self.left_part_frame.rowconfigure(0, weight=1)
        self.left_part_frame.rowconfigure((1, 2, 3), weight=3)

        self.line1.grid(row=0, column=0, stick='news', padx=20, pady=10)
        self.line2.grid(row=1, column=0, stick='news', padx=20, pady=10)
        self.line3.grid(row=2, column=0, stick='news', padx=20, pady=10)
        self.line4.grid(row=3, column=0, stick='news', padx=20, pady=10)


    def run_alg_(self):
        # TODO: добавить обработку для нескольких многоугольников
        # TODO: Добавить каст кругов к многоугольникам.
        # Получим многоугольник.

        try:
            poly = self.autocad.get_polygons()
        except:
            MsgBox.show_error_msgbox('Не удалось получить многоугольник(и). \nПрервите все активные команды и попробуйте снова.')
            return

        # Получим параметры алгоритма.
        try:
            R = self.get_entry_('R')
            alpha_res = self.get_entry_('ALPHA_RESOLUTION')
            res = self.get_entry_('RESOLUTION')
            # ---
            iterations_mult_del = self.get_entry_('ITERATIONS_MULT_DELETION')
            iterations_mult_moving = self.get_entry_('ITERATIONS_MULT_MOVING')
            INNER_BOUND = self.get_entry_('INNER_BOUND')
            move_schedule_mult = self.get_entry_('MOVE_SCHEDULE_MULT')
            # ---
            angle_res = self.get_entry_('ANGLE_RESOLUTION')
            move_mult = self.get_entry_('MOVE_MULTIPLIER')
            self_inter = self.get_entry_('SELF_INTER')
            outside = self.get_entry_('OUTSIDE')
            coverage = self.get_entry_('COVERAGE')
            del_circle_count = self.get_entry_('DEL_CIRCLE_COUNT')
            circle_count = self.get_entry_('CIRCLE_COUNT')
        except:
            print('Parsing exception')
            return

        # Запустим алгоритм.

        # Построим покрытие шестиугольной сеткой.
        hex_alg = HexagonalAlgorithm(poly, R)  # Укажем данные.
        hex_alg.set_params(
            hex_alg=hexagonal_np,
            ALPHA_RESOLUTION=alpha_res,
            RESOLUTION=res
        )  # Укажем параметры решения.
        hex_alg.run_algorithm()  # Запустим алгоритм.
        hex_ans = hex_alg.get_result()  # Получим результат - list[Circle].

        # Разложим круги по уровням дальности до края многоугольника
        layers = get_layers(poly, hex_ans)

        # Выделим "внутренние" круги.
        inners = np.zeros(len(layers))
        inners[layers >= INNER_BOUND] = 1

        # Починим методом ветвей и границ.
        bnb_alg = FlexibleBnBAlgorithm(poly, hex_ans)
        # Запустим алгоритм с приоритетом на удаление кругов.
        bnb_alg.set_params(
            max_iterations=int(np.ceil(iterations_mult_del * len(hex_ans))),
            params=StretchedBnBParams(
                poly,
                len(hex_ans),
                MOVE_SCHEDULE=(lambda x: move_schedule_mult * x),
                SELF_INTER_W=self_inter,
                OUTSIDE_W=outside,
                CIRCLE_COUNT_W=del_circle_count,
                COVERAGE_W=coverage,
                ANGLE_RESOLUTION=angle_res,
                MOVE_MULTIPLIER=move_mult),
            fixed=list(inners)
        )
        bnb_alg.run_algorithm()

        # Запустим алгоритм с приоритетом на перемещение кругов.
        bnb_alg.params.CIRCLE_COUNT_W = circle_count
        bnb_alg.set_params(
            max_iterations=int(np.ceil(iterations_mult_moving * len(bnb_alg.circles))))
        bnb_alg.run_algorithm()
        circles = bnb_alg.get_result()

        # Вернём ответ.
        try:
            self.autocad.draw_circles(circles)
        except:
            MsgBox.show_error_msgbox('Не удалось отрисовать покрытие. \nПрервите все активные команды и попробуйте снова.')
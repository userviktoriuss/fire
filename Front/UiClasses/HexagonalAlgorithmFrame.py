from Algorithms.Hexagonal.HexagonalAlgorithm import HexagonalAlgorithm
from Algorithms.Hexagonal.hexagonal_coverings import hexagonal_np
from Algorithms.RedundantRemovers.GeneticRedundantRemover import GeneticRedundantRemover
from Algorithms.RedundantRemovers.GreedyRedundantRemover import GreedyRedundantRemover
from Front.Extractor import Exctractor
from Front.Fonts import Fonts
from Front.UiClasses.AlgorithmFrame import AlgorithmFrame, TextInfo
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from Front.UiClasses.MsgBox import MsgBox


class HexagonalAlgorithmFrame(AlgorithmFrame):
    '''
    Класс для страницы покрытия методом Шестиугольной сетки.

    Определяет описание алгоритма, поля заполнения параметров и
    вызов алгоритма с заданными параметрами.
    '''
    title = 'Шестиугольная сетка'
    text_info = TextInfo(
        description=
        '''Этот алгоритм предназначен для покрытия многоугольников с помощью метода шестиугольной сетки. Хорошо покрывает симметричные фигуры правильной формы, габариты которых не сильно отличаются от чисел вида R*k.
Также после метода можно попробовать оптимизировать количество кругов. Есть два алгоритма: жадный и генетический.
        ''',
        params=
        '''· R - радиус кругов, которыми покрывается многоугольник.
· ALPHA_RESOLUTION - сколько разных углов от 0 до π/3 будет перебирать алгоритм.
· RESOLUTION - сколько сдвигов будет перебирать алгоритм.
Алгоритмы оптимизации количества кругов:
· Жадный алгоритм оставляет круги, центры которых лежат внутри многоугольника. Из оставшихся берёт только те, что имеют достаточно большое пересечение с многоугольником.
· Генетический алгоритм пытается максимизировать площадь покрытия и минимизировать площадь кругов вне круга, а также суммарную площадь их попарного пересечения.
''',
        recommended_values=
        '''· ALPHA_RESOLUTION, RESOLUTION не стоит брать большими, 1-3 вполне достаточно.
· Алгоритмы оптимизации заметно увеличивают время работы. Генетический алгоритм в среднем работает лучше жадного, но дольше.
''',
        notes=
        '''Может создавать лишние круги на границе многоугольника.
'''
    )

    removers = {
        'Генетический алгоритм': GeneticRedundantRemover,
        'Жадный алгоритм': GreedyRedundantRemover
    }

    def fill_left_panel_(self):
        self.line1 = ctk.CTkFrame(self.left_panel)
        self.line2 = ctk.CTkFrame(self.left_panel)
        self.line3 = ctk.CTkFrame(self.left_panel)

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
        self.line3.columnconfigure(1, weight=2)
        self.line3.rowconfigure((0, 1), weight=1)

        self.add_checkbox('DO_REMOVE', self.line3, 'Убрать лишние круги', self.activate_remover_choice_, 0)
        self.add_label_combobox_pair_('REMOVER', self.line3, 'Способ:', list(self.removers.keys()), 1)
        self.activate_remover_choice_()

        # grid ------------------------------------------------------------
        # Расположим все строки в левой части.
        self.left_part_frame.columnconfigure(0, weight=1)
        self.left_part_frame.rowconfigure(0, weight=1)
        self.left_part_frame.rowconfigure((1, 2), weight=4)

        self.line1.grid(row=0, column=0, stick='news', padx=20, pady=10)
        self.line3.grid(row=2, column=0, stick='news', padx=20, pady=10)
        self.line2.grid(row=1, column=0, stick='news', padx=20, pady=10)

    def activate_remover_choice_(self):
        self.__dict__[self.combobox_name_('REMOVER')]\
            .configure(state='disabled' if self.get_('DO_REMOVE') == 0 else 'readonly')

    def run_alg_(self):
        # TODO: добавить обработку для нескольких многоугольников
        # TODO: Добавить каст кругов к многоугольникам.
        # Получим многоугольник.
        # poly = None

        try:
            poly = self.autocad.get_polygons()
        except:
            MsgBox.show_error_msgbox('Не удалось получить многоугольник(и). \nПрервите все активные команды и попробуйте снова.')
            return

        # Получим параметры алгоритма.
        try:
            R = self.get_('R')
            alpha_res = self.get_('ALPHA_RESOLUTION')
            res = self.get_('RESOLUTION')
        except:
            return

        remove_redundant = self.get_('DO_REMOVE') == 1

        remover = self.get_('REMOVER')

        # Запустим алгоритм.
        hex_alg = HexagonalAlgorithm(poly, R)  # Укажем данные.
        hex_alg.set_params(
            hex_alg=hexagonal_np,
            ALPHA_RESOLUTION=alpha_res,
            RESOLUTION=res,
        )  # Укажем параметры решения.
        hex_alg.run_algorithm()  # Запустим алгоритм.
        circles = hex_alg.get_result()

        if remove_redundant:
            # Получим выбранный алгоритм по имени.
            remover_alg = self.removers[remover](poly, circles)
            # Запустим алгоритм.
            remover_alg.run_algorithm()
            # Получим ответ.
            circles = remover_alg.get_result()

        try:
            self.autocad.draw_circles(circles)
        except:
            MsgBox.show_error_msgbox('Не удалось отрисовать покрытие. \nПрервите все активные команды и попробуйте снова.')


from Algorithms.Hexagonal.HexagonalAlgorithm import HexagonalAlgorithm
from Algorithms.Hexagonal.hexagonal_coverings import hexagonal_np
from Algorithms.RedundantRemovers.GeneticRedundantRemover import GeneticRedundantRemover
from Algorithms.RedundantRemovers.GreedyRedundantRemover import GreedyRedundantRemover
from Front.Extractor import Exctractor
from Front.Fonts import Fonts
from Front.UiClasses.AlgorithmFrame import AlgorithmFrame, TextInfo
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox


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
        self.r_label = ctk.CTkLabel(self.line2, text='R', font=Fonts.label_font)
        self.r_input = ctk.CTkEntry(self.line2)
        self.alpha_res_label = ctk.CTkLabel(self.line2, text='ALPHA_RESOLUTION', font=Fonts.label_font)
        self.alpha_res_input = ctk.CTkEntry(self.line2)
        self.res_label = ctk.CTkLabel(self.line2, text='RESOLUTION', font=Fonts.label_font)
        self.res_input = ctk.CTkEntry(self.line2)

        self.r_label.grid(row=0, column=0, sticky='w', padx=10)
        self.r_input.grid(row=0, column=1, columnspan=2, sticky='e')
        self.alpha_res_label.grid(row=1, column=0, sticky='w', padx=10)
        self.alpha_res_input.grid(row=1, column=1, columnspan=2, sticky='e')
        self.res_label.grid(row=2, column=0, sticky='w', padx=10)
        self.res_input.grid(row=2, column=1, columnspan=2, sticky='e')
        # line3 ---------------------------------------------------------
        self.line3.columnconfigure((0, 1, 2), weight=1)
        self.line3.rowconfigure((0, 1), weight=1)
        self.remove_unnec_circles = ctk.CTkCheckBox(self.line3, text='Убрать лишние круги',
                                                    command=self.activate_remover_choice_,
                                                    font=Fonts.label_font)
        self.remover_label = ctk.CTkLabel(self.line3, text='Способ:', font=Fonts.label_font)
        self.remover = ctk.CTkComboBox(self.line3, values=list(self.removers.keys()), font=Fonts.label_font)
        self.activate_remover_choice_()

        self.remove_unnec_circles.grid(row=0, column=0, columnspan=3, sticky='w')
        self.remover_label.grid(row=1, column=0, sticky='w')
        self.remover.grid(row=1, column=1, columnspan=2, sticky='we')
        # grid ------------------------------------------------------------
        # Расположим все строки в левой части.
        self.left_part_frame.columnconfigure(0, weight=1)
        self.left_part_frame.rowconfigure(0, weight=1)
        self.left_part_frame.rowconfigure((1, 2), weight=4)

        self.line1.grid(row=0, column=0, stick='news', padx=20, pady=10)
        self.line3.grid(row=2, column=0, stick='news', padx=20, pady=10)
        self.line2.grid(row=1, column=0, stick='news', padx=20, pady=10)

    def activate_remover_choice_(self):
        self.remover.configure(state='disabled' if self.remove_unnec_circles.get() == 0 else 'readonly')

    def run_alg_(self):
        # TODO: добавить обработку для нескольких многоугольников
        # TODO: Добавить каст кругов к многоугольникам.
        # Получим многоугольник.
        # poly = None

        try:
            poly = self.autocad.get_polygons()
        except:
            CTkMessagebox(title='Ошибка!',
                          message='Не удалось получить многоугольник(и). \n' + \
                                  'Прервите все активные команды и попробуйте снова.',
                          icon='cancel',
                          width=580,
                          font=Fonts.text_font)
            return
            pass

        # Получим параметры алгоритма.
        try:
            R = Exctractor.get_float(self.r_input.get(), 'R')
            alpha_res = Exctractor.get_int(self.alpha_res_input.get(), 'ALPHA_RESOLUTION')
            res = Exctractor.get_int(self.res_input.get(), 'RESOLUTION')
        except:
            return

        remove_redundant = self.remove_unnec_circles.get() == 1

        remover = self.remover.get()

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
            CTkMessagebox(title='Ошибка!',
                          message='Не удалось отрисовать покрытие. \n' + \
                                  'Прервите все активные команды и попробуйте снова.',
                          icon='cancel',
                          width=580,
                          font=Fonts.text_font)


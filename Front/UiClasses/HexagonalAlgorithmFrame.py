import tkinter as tk

from Algorithms.Hexagonal.HexagonalAlgorithm import HexagonalAlgorithm
from Algorithms.Hexagonal.hexagonal_coverings import hexagonal_np
from Front.UiClasses.AlgorithmFrame import AlgorithmFrame, TextInfo
import ttkbootstrap as btrp
import customtkinter as ctk


class HexagonalAlgorithmFrame(AlgorithmFrame):
    '''
    Класс для страницы алгоритма.

    Определяет описание алгоритма, поля заполнения параметров и
    вызов алгоритма с заданными параметрами.
    '''
    title = 'Шестиугольная сетка'
    text_info = TextInfo(
        description=
        '''Этот алгоритм предназначен для покрытия многоугольников с помощью метода шестиугольной сетки.
        Хорошо покрывает симметричные фигуры правильной формы, габариты которых не сильно отличаются от чисел вида R*k.
        ''',
        # TODO: логичный порядок
        params=
        '''· ALPHA - задаёт в радианах поворот шестиугольной сетки вокруг стартовой точки.
        · R - радиус кругов, которыми покрывается многоугольник.
        · Sx - смещение сетки вдоль оси абсцисс.
        · Sy - смещение сетки вдоль оси ординат.
        ''',
        recommended_values=
        '''· ALPHA - в зависимости от поворота фигуры, но обязательно 0 ≤ ALPHA ≤ π/3.
        · (Sx, Sy) точка внутри фигуры или на границе.
        ''',
        notes=
        '''Может создавать лишние круги на границе многоугольника.
        '''
    )

    def fill_left_panel_(self):
        self.line1 = ctk.CTkFrame(self.left_panel)
        self.line2 = ctk.CTkFrame(self.left_panel)
        self.line3 = ctk.CTkFrame(self.left_panel)
        self.line4 = ctk.CTkFrame(self.left_panel)

        # line1 --------------------------------------------------------
        self.alg_label = ctk.CTkLabel(self.line1, text=self.title, font=('bold', 20))
        self.alg_label.pack(side='top')
        # line2 --------------------------------------------------------
        self.line2.columnconfigure(0, weight=1)
        self.line2.columnconfigure(1, weight=4)
        self.line2.rowconfigure((0, 1), weight=1)
        self.alpha_label = ctk.CTkLabel(self.line2, text='ALPHA')
        self.r_label = ctk.CTkLabel(self.line2, text='R')
        self.alpha_input = ctk.CTkEntry(self.line2)
        self.r_input = ctk.CTkEntry(self.line2)

        self.r_label.grid(row=0, column=0, sticky='w', padx=10)
        self.r_input.grid(row=0, column=1, columnspan=2, sticky='w')
        self.alpha_label.grid(row=1, column=0, sticky='w', padx=10)
        self.alpha_input.grid(row=1, column=1, columnspan=2, sticky='w')

        # line3 ---------------------------------------------------------
        self.line3.columnconfigure(0, weight=1)
        self.line3.columnconfigure(1, weight=4)
        self.line3.rowconfigure((0, 1), weight=1)
        self.sx_label = ctk.CTkLabel(self.line3, text='Sx')
        self.sy_label = ctk.CTkLabel(self.line3, text='Sy')
        self.sx_input = ctk.CTkEntry(self.line3)
        self.sy_input = ctk.CTkEntry(self.line3)

        self.sx_label.grid(row=0, column=0, sticky='w', padx=10)
        self.sx_input.grid(row=0, column=1, columnspan=2, sticky='w')
        self.sy_label.grid(row=1, column=0, sticky='w', padx=10)
        self.sy_input.grid(row=1, column=1, columnspan=2, sticky='w')

        # line4 -----------------------------------------------------------
        # TODO: maybe?
        #self.line4.rowconfigure((0, 1), weight=1)
        #self.remove_unnec_circles = ctk.CTkCheckBox(self.line4, text='Убрать лишние круги', command=self.activate_remover_choice_)
        #self.remover = ctk.CTkComboBox(self.line4, values=[])
        # grid ------------------------------------------------------------
        # Расположим все строки в левой части.
        self.left_part_frame.rowconfigure(0, weight=1)
        self.left_part_frame.rowconfigure((1, 2, 3), weight=3)

        self.line1.grid(row=0, column=0, stick='news', padx=20, pady=10)
        self.line3.grid(row=2, column=0, stick='news', padx=20, pady=10)
        self.line2.grid(row=1, column=0, stick='news', padx=20, pady=10)
        self.line4.grid(row=3, column=0, stick='news', padx=20, pady=10)
        # TODO: накидать UI
        pass

    def activate_remover_choice_(self):
        if self.remove_unnec_circles.get() == 1:
            self.remover.state

    def run_alg_(self):
        # TODO: получить многоугольник(и), запустить алгоритм, вернуть кружочки.
        # TODO: добавить обработку для нескольких многоугольников
        # TODO: Добавить каст кругов к многоугольникам.
        # TODO: Добавить обработку исключений.
        # Получим многоугольник.
        poly = self.autocad.get_polygons()

        # Получим параметры алгоритма.
        R = float(self.r_input.get())
        alpha = float(self.alpha_input.get())
        sx = float(self.sx_input.get())
        sy = float(self.sy_input.get())

        # Запустим алгоритм.
        hex_alg = HexagonalAlgorithm(poly, R)  # Укажем данные.
        hex_alg.set_params(
            hex_alg=hexagonal_np,
            REMOVE_REDUNDANT=False,
            ALPHA_RESOLUTION=5,
            RESOLUTION=5
        )  # Укажем параметры решения.
        hex_alg.run_algorithm()  # Запустим алгоритм.
        hex_ans = hex_alg.get_result()

        self.autocad.draw_circles(hex_ans)

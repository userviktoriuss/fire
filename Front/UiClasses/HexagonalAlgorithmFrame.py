import tkinter as tk
from Front.UiClasses.AlgorithmFrame import AlgorithmFrame, TextInfo
import ttkbootstrap as btrp
import customtkinter as ctk


class HexagonalAlgorithmFrame(AlgorithmFrame):
    title = 'Шестиугольная сетка'
    text_info = TextInfo(
        description=
        '''Этот алгоритм предназначен для покрытия многоугольников с помощью метода шестиугольной сетки.
        Хорошо покрывает симметричные фигуры правильной формы, габариты которых не сильно отличаются от чисел вида r*k.
        ''',
        params=
        '''· ALPHA задаёт в радианах поворот шестиугольной сетки вокруг стартовой точки.
        · A задаёт сторону шестиугольников.
        · Sx задаёт смещение сетки вдоль оси абсцисс.
        · Sy задаёт смещение сетки вдоль оси ординат.
        ''',
        recommended_values=
        '''· ALPHA - в зависимости от поворота фигуры, но обязательно 0 ≤ ALPHA ≤ π/3.
        · A = r - радиус кругов.
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
        self.a_label = ctk.CTkLabel(self.line2, text='A')
        self.alpha_input = ctk.CTkEntry(self.line2)
        self.a_input = ctk.CTkEntry(self.line2)

        self.a_label.grid(row=0, column=0, sticky='w', padx=10)
        self.a_input.grid(row=0, column=1, columnspan=2, sticky='w')
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

        # Расположим все строки в левой части
        self.left_part_frame.rowconfigure(0, weight=1)
        self.left_part_frame.rowconfigure((1, 2, 3), weight=3)

        self.line1.grid(row=0, column=0, stick='news', padx=20, pady=10)
        self.line3.grid(row=2, column=0, stick='news', padx=20, pady=10)
        self.line2.grid(row=1, column=0, stick='news', padx=20, pady=10)
        self.line4.grid(row=3, column=0, stick='news', padx=20, pady=10)
        # TODO: накидать UI
        pass

    def run_alg_(self):
        # TODO: получить многоугольник(и), запустить алгоритм, вернуть кружочки.
        pass

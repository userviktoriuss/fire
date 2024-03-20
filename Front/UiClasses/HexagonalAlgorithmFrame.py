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
        self.line1 = btrp.Frame(self.left_panel)
        self.line2 = btrp.Frame(self.left_panel)
        self.line3 = btrp.Frame(self.left_panel)
        self.line4 = btrp.Frame(self.left_panel)

        # line1 --------------------------------------------------------
        self.alg_label = btrp.Label(self.line1, text=self.title, font=('bold', 20))
        self.alg_label.pack(side='top')
        # line2 --------------------------------------------------------
        self.line2.columnconfigure(0, weight=1)
        self.line2.columnconfigure(1, weight=2)
        self.line2.rowconfigure((0, 1), weight=1)
        self.alpha_label = btrp.Label(self.line2, text='ALPHA')
        self.a_label = btrp.Label(self.line2, text='A')
        self.alpha_input = ctk.CTkEntry(self.line2)
        self.a_input = ctk.CTkEntry(self.line2)

        self.a_label.grid(row=0, column=0, stick='w')
        self.a_input.grid(row=0, column=1, columnspan=2, stick='w')
        self.alpha_label.grid(row=1, column=0, stick='w')
        self.alpha_input.grid(row=1, column=1, columnspan=2, stick='w')

        # line3 ---------------------------------------------------------
        self.line1.pack(side='top', fill='x')
        self.line2.pack(side='top', fill='both')
        self.line3.pack(side='top', fill='x')
        self.line4.pack(side='top', fill='x')
        # TODO: накидать UI
        pass

    def run_alg_(self):
        # TODO: получить многоугольник(и), запустить алгоритм, вернуть кружочки.
        pass

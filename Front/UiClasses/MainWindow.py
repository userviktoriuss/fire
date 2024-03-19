import tkinter as tk
from tkinter import ttk

from Back.AutoCadFacade import AutoCadFacade
from Front.UiClasses.HexagonalAlgorithmFrame import HexagonalAlgorithmFrame
from Front.UiClasses.MainFrame import MainFrame


class MainWindow(tk.Tk):
    def __init__(self, title, geometry):
        super().__init__()
        self.title(title)
        self.geometry(geometry)
        # Инициализировать AutoCad нужно ДО UI, т.к. они берут ссылку на открытый чертёж.
        # Отдавать фреймам весь MainWindow плохо.
        self.setup_autocad()
        self.setup_ui()


    def setup_ui(self):
        self.notebook = ttk.Notebook(
            self,
            width=300, #self.winfo_width(),
            height=200)# self.winfo_height())

        self.main_frame = MainFrame(self.notebook, self.autocad)
        self.hexagonal_frame = HexagonalAlgorithmFrame(self.notebook, self.autocad)

        self.main_frame.pack(padx=5, pady=5, side='left', fill='both')
        self.hexagonal_frame.pack(padx=5, pady=5)
        # TODO: другие алгоритмы
        # TODO: Задать алгоритмам один интерфейс - мб, пронаследовать от какго-то абстрактного
        # TODO: захардкодить алгоритмам секции описания
        # TODO: добавить скроллинг для правой секции, если описание слишком длинное

        self.notebook.add(self.main_frame, text='Главная')
        self.notebook.add(self.hexagonal_frame, text='Шестиугольное покрытие')

        self.notebook.pack(padx=5, pady=5, side='left', fill='both', expand=True)
        self.notebook.enable_traversal()

    def setup_autocad(self):
        self.autocad = AutoCadFacade()
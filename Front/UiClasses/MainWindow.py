import tkinter as tk
import tkinter.ttk as ttk

import Back.AutoCadFacade as acf
import Front.UiClasses.HexagonalAlgorithmFrame as haf
import Front.UiClasses.MainFrame as mf
from Front.Settings import ColorScheme


class MainWindow(tk.Tk):
    def __init__(self, title, geometry):
        super().__init__()
        self.title(title)
        self.geometry(geometry)
        self.resizable(False, False)
        self.setup_autocad()
        self.setup_ui()


    def setup_ui(self):
        self.configure(background=ColorScheme.BG_COLOR)
        self.notebook = ttk.Notebook(self, width=300, height=200)

        self.algs = [
            haf.HexagonalAlgorithmFrame(self.notebook, self.autocad),
            haf.HexagonalAlgorithmFrame(self.notebook, self.autocad), # TODO: change
            haf.HexagonalAlgorithmFrame(self.notebook, self.autocad), # TODO: change
            haf.HexagonalAlgorithmFrame(self.notebook, self.autocad) # TODO: change
        ]
        self.main_frame = mf.MainFrame(self.notebook, self)
        self.main_frame.pack(padx=5, pady=5, side='left', fill='both')

        for alg in self.algs:
            alg.pack(padx=5, pady=5)

        # TODO: другие алгоритмы
        # TODO: Задать алгоритмам один интерфейс - мб, пронаследовать от какго-то абстрактного
        # TODO: захардкодить алгоритмам секции описания
        # TODO: добавить скроллинг для правой секции, если описание слишком длинное

        self.notebook.add(self.main_frame, text='Главная')
        for alg in self.algs:
            self.notebook.add(alg, text=alg.title)

        self.notebook.pack(side='left', fill='both', expand=True)
        self.notebook.enable_traversal()

    def setup_autocad(self):
        self.autocad = acf.AutoCadFacade()
import ttkbootstrap as btrp
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

import Back.AutoCadFacade as acf
import Front.UiClasses.HexagonalAlgorithmFrame as haf
import Front.UiClasses.MainFrame as mf
from Front.Fonts import Fonts
from Front.Settings import ICON, FONT, TAB_TEXT_SIZE, MENU_TEXT_SIZE
from Front.UiClasses.HexGeneticAlgorithmFrame import HexGeneticAlgorithmFrame


class MainWindow(ctk.CTk):
    def __init__(self, title, geometry):
        super().__init__()
        self.title(title)
        self.geometry(geometry)
        self.setup_autocad()
        Fonts.setup_fonts()
        self.setup_ui()
        self.minsize(660, 480)

    def setup_ui(self):
        self.config_menu()
        s = btrp.Style()
        s.configure('TNotebook.Tab', font=(FONT, str(TAB_TEXT_SIZE)))
        self.notebook = btrp.Notebook(self, width=300, height=200)

        self.algs = [
            haf.HexagonalAlgorithmFrame(self.notebook, self.autocad),
            HexGeneticAlgorithmFrame(self.notebook, self.autocad),
            haf.HexagonalAlgorithmFrame(self.notebook, self.autocad),  # TODO: change
            haf.HexagonalAlgorithmFrame(self.notebook, self.autocad)  # TODO: change
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

    def config_menu(self):
        fnt = (FONT, MENU_TEXT_SIZE)
        self.menu = btrp.Menu(self, font=fnt)
        self.file_menu = btrp.Menu(self.menu, tearoff=0, font=fnt)

        self.file_menu.add_command(label='Сохранить параметры', command=self.save_params_)
        self.file_menu.add_command(label='Сохранить параметры как', command=self.save_params_as_)
        self.file_menu.add_command(label='Загрузить параметры', command=self.load_params_)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Выйти', command=self.quit)

        self.menu.add_cascade(menu=self.file_menu, label='Файл', font=fnt)
        self.config(menu=self.menu)

        self.menu.add_command(command=self.show_info_msgbox_, label='О программе', font=fnt)

    def save_params_(self):
        pass  # TODO:

    def save_params_as_(self):
        pass  # TODO:

    def load_params_(self):
        pass  # TODO:

    def show_info_msgbox_(self):
        CTkMessagebox(title='О программе',
                      message='-= Дополнение для AutoCAD =-\n\n' + \
                              'Версия 1.0\n\n' + \
                              'Филимонов Виктор, 2024',
                      icon=ICON,
                      width=580,
                      font=Fonts.text_font)  # TODO:

    def setup_autocad(self):
        self.autocad = acf.AutoCadFacade()

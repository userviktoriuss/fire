import json
import tkinter as tk
import tkinter.filedialog

import ttkbootstrap as btrp
import customtkinter as ctk

import Back.AutoCadFacade as acf
import Front.UiClasses.HexagonalAlgorithmFrame as haf
import Front.UiClasses.MainFrame as mf
from Front.Fonts import Fonts
from Front.Settings import FONT, TAB_TEXT_SIZE, MENU_TEXT_SIZE, PARAMS_PATH
from Front.UiClasses.HexGeneticAlgorithmFrame import HexGeneticAlgorithmFrame
from Front.UiClasses.MsgBox import MsgBox
from Front.UiClasses.RkGeneticAlgorithmFrame import RkGeneticAlgorithmFrame


class MainWindow(ctk.CTk):
    open_file = None

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

        self.algs = []
        self.algs.append(haf.HexagonalAlgorithmFrame(self.notebook, self.autocad))
        self.algs.append(HexGeneticAlgorithmFrame(self.notebook, self.autocad))
        self.algs.append(RkGeneticAlgorithmFrame(self.notebook, self.autocad))  # TODO: change
        self.algs.append(haf.HexagonalAlgorithmFrame(self.notebook, self.autocad))  # TODO: change
        self.main_frame = mf.MainFrame(self.notebook, self)
        self.main_frame.pack(padx=5, pady=5, side='left', fill='both')

        for alg in self.algs:
            alg.pack(padx=5, pady=5)

        # TODO: другие алгоритмы
        # TODO: захардкодить алгоритмам секции описания

        self.notebook.add(self.main_frame, text='Главная')
        for alg in self.algs:
            self.notebook.add(alg, text=alg.title)

        self.notebook.pack(side='left', fill='both', expand=True)
        self.notebook.enable_traversal()

        # Загрузим параметры по умолчанию
        self.load_params_()

    def config_menu(self):
        fnt = (FONT, MENU_TEXT_SIZE)
        self.menu = btrp.Menu(self, font=fnt)
        self.file_menu = btrp.Menu(self.menu, tearoff=0, font=fnt)

        self.file_menu.add_command(label='Открыть', command=self.open_params_)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Сохранить', command=lambda: self.save_params_(path=self.open_file))
        self.file_menu.add_command(label='Сохранить как', command=self.save_params_as_)
        self.file_menu.add_command(label='Назначить по умолчанию',
                                   command=lambda: self.save_params_(path=PARAMS_PATH))
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Выйти', command=self.quit)

        self.menu.add_cascade(menu=self.file_menu, label='Файл', font=fnt)
        self.config(menu=self.menu)

        self.menu.add_command(command=MsgBox.show_about_program_msgbox_, label='О программе', font=fnt)

    # Загружает параметры из файла.
    def load_params_(self, path=None):
        if path is None:
            path = PARAMS_PATH

        self.open_file = path

        d = None
        try:
            with open(path, 'r') as f:
                d = json.load(f)
        except:
            MsgBox.show_error_msgbox('Не удалось загрузить параметры из файла. Возможно, это не json-файл.')

        for i in range(len(self.algs)):
            # if i > 2:
            #     continue  # TODO: убрать!!!! это тест!!!
            for name in d[str(i)]:
                val = d[str(i)][name]
                self.algs[i].params.update(name, val)
                self.algs[i].set_(name, val)  # TODO: заработает?

        pass

    # Сохранить текущие параметры в файл.
    def save_params_(self, path):
        d = dict()
        for i in range(len(self.algs)):
            # TODO: убрать!!!!!
            d[str(i)] = dict()
            # if i > 2:
            #     continue
            try:
                self.algs[i].update_all_params_()
            except:
                return
            d[str(i)] = self.algs[i].params.get_one_dict()

        try:
            with open(path, 'w') as f:
                json.dump(d, f)
        except:
            MsgBox.show_error_msgbox('Не удалось сохранить параметры.')

    # Сохранить текущие параметры в отдельный файл.
    def save_params_as_(self):
        path = tk.filedialog.asksaveasfilename(defaultextension=".json")
        if not path.endswith('.json'):
            path += '.json'
        if path is None or path == '':
            return
        self.open_file = path
        self.save_params_(path)

    # Загрузить параметры из файла.
    def open_params_(self):
        path = tk.filedialog.askopenfilename(defaultextension=".json", filetypes=(("json files","*.json"),))
        if path is None or path == '':
            return
        self.load_params_(path)

    def setup_autocad(self):
        self.autocad = acf.AutoCadFacade()

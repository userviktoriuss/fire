from tkinter.constants import END

import Back.AutoCadFacade as acf
import customtkinter as ctk
import ttkbootstrap as btrp

from Front.Extractor import Exctractor
from Front.Fonts import Fonts


class TextInfo():
    def __init__(self,
                 description,
                 params,
                 recommended_values,
                 notes):
        self.description = description
        self.params = params
        self.recommended_values = recommended_values
        self.notes = notes


class DescriptionFrame(ctk.CTkTextbox):
    def __init__(self,
                 master,
                 text_info: TextInfo):
        super().__init__(master, font=Fonts.text_font)

        text = '-= Описание =-\n' + text_info.description + '\n' + \
               '-= Параметры =-\n' + text_info.params + '\n' + \
               '-= Рекомендуемые значения =-\n' + text_info.recommended_values + '\n' + \
               '-= Примечание =-\n' + text_info.notes
        self.insert(END, text)
        self.configure(state='disabled')


class Params:
    choose_ = dict()

    def __init__(self):
        self.choose_[int] = dict()
        self.choose_[float] = dict()
        self.choose_[str] = dict()

    def put(self, name: str, value: 'instance of the type', type_: 'the type'):
        self.choose_[type_][name] = value

    def update(self, name: str, value: 'instance of the type'):
        self.choose_[self.get_type(name)][name] = value

    def get(self, name: str):
        return self.choose_[self.get_type(name)][name]

    def get_type(self, name: str):
        for key in self.choose_:
            if name in self.choose_[key].keys():
                type_ = key
                break
        else:
            raise Exception('Параметр не задан')
        return type_

    def get_one_dict(self):
        res = dict()
        for key in self.choose_:
            res = res | self.choose_[key]
        return res


class AlgorithmFrame(btrp.Frame):
    title = 'Алгоритм'
    text_info = TextInfo(
        description=
        '''
        Описание.
        ''',
        params=
        '''
        Параметры.
        ''',
        recommended_values=
        '''
        Рекомендованные значение.
        ''',
        notes=
        '''
        Примечание.
        '''
    )

    params = Params()

    def __init__(self, master, autocad: acf.AutoCadFacade):
        super().__init__(master)
        self.autocad = autocad

        self.left_part_frame = ctk.CTkFrame(self, bg_color='white', fg_color='white')  # ну вот ему пофиг просто
        self.left_panel = ctk.CTkFrame(self.left_part_frame,
                                       background_corner_colors=('white', 'white', 'white', 'white'))
        self.fill_left_panel_()
        self.right_part_frame = DescriptionFrame(self, self.text_info)

        self.run_button = ctk.CTkButton(self.left_part_frame, text='Запустить алгоритм', command=self.run_alg_,
                                        font=Fonts.button_font)

        self.left_panel.pack(expand=True, side='top', fill='both')
        self.run_button.pack(side='bottom', pady=5)

        self.columnconfigure((0, 1), weight=1, uniform='a')
        self.rowconfigure(0, weight=1)
        self.left_part_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        self.right_part_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)

    def label_name_(self, name: str):
        return f'{name}_label'

    def entry_name_(self, name: str):
        return f'{name}_entry'

    def add_label_input_pair_(self, name: str, frame: ctk.CTkFrame, row: int, type_: 'the type' = float):
        self.params.put(name, type_('0'), type_)

        self.__dict__[self.label_name_(name)] = ctk.CTkLabel(frame, text=name, font=Fonts.label_font)
        self.__dict__[self.entry_name_(name)] = ctk.CTkEntry(frame)
        self.__dict__[self.label_name_(name)].grid(row=row, column=0, sticky='w', padx=10)
        self.__dict__[self.entry_name_(name)].grid(row=row, column=1, columnspan=2, sticky='e')
        # TODO: check that works ok

    def get_entry_(self, name: str):
        # TODO: Найти в проекте type и заменить, чтобы не было shadowing
        type_ = self.params.get_type(name)
        val = Exctractor.get(type_, self.__dict__[self.entry_name_(name)].get(), name)
        self.params.update(name, val)
        return val

    def set_entry_(self, name: str, val: str):
        self.__dict__[self.entry_name_(name)].delete(0, END)
        self.__dict__[self.entry_name_(name)].insert(0, val)

    def update_all_params_(self):
        for type_ in self.params.choose_:
            for name in self.params.choose_[type_]:
                val = Exctractor.get(type_, self.__dict__[self.entry_name_(name)].get(), name)
                self.params.update(name, val)

    def fill_left_panel_(self):
        pass

    def run_alg_(self):
        pass

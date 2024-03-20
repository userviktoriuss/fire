from tkinter.constants import END
from tkinter.scrolledtext import ScrolledText

import Back.AutoCadFacade as acf
import customtkinter as ctk
import ttkbootstrap as btrp


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


class DescriptionFrame(ScrolledText):
    def __init__(self,
                 master,
                 text_info: TextInfo):
        super().__init__(master)
        text = '-= Описание =-\n' + text_info.description + '\n' + \
               '-= Параметры =-\n' + text_info.params + '\n' + \
               '-= Рекомендованные значения =-\n' + text_info.recommended_values + '\n' + \
               '-= Примечание =-\n' + text_info.notes
        self.insert(END, text)

        # self.text_info = text_info
        # self.description = btrp.Label(self, text='Описание.\n' + text_info.description)
        # self.params = btrp.Label(self, text='Параметры.\n' + text_info.params)
        # self.recommended_values = btrp.Label(self, text='Рекомендованные значения.\n' + text_info.recommended_values)
        # self.notes = btrp.Label(self, text='Примечание.\n' + text_info.notes)
        # self.description.pack(expand=True, side='top', fill='x')
        # self.params.pack(expand=True, side='top', fill='x')
        # self.recommended_values.pack(expand=True, side='top', fill='x')
        # self.notes.pack(expand=True, side='top', fill='x')


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

    def __init__(self, master, autocad: acf.AutoCadFacade):
        super().__init__(master)
        self.autocad = autocad

        self.left_part_frame = btrp.Frame(self)
        self.left_panel = ctk.CTkFrame(self.left_part_frame)
        self.fill_left_panel_()
        self.right_part_frame = DescriptionFrame(self, self.text_info)

        self.run_button = btrp.Button(self.left_part_frame, text='Запустить алгоритм.', command=self.run_alg_)

        self.left_panel.pack(expand=True, side='top', fill='x')
        self.run_button.pack(side='bottom')

        self.columnconfigure((0, 1), weight=1, uniform='a')
        self.rowconfigure(0, weight=1)
        self.left_part_frame.grid(row=0, column=0, sticky='nsew')
        self.right_part_frame.grid(row=0, column=1, sticky='nsew')
        #self.left_part_frame.pack(expand=True, side='left', fill='both', padx=5, pady=5)
        #self.right_part_frame.pack(expand=True, side='right', fill='both', padx=5, pady=5)

    def fill_left_panel_(self):
        pass

    def run_alg_(self):
        pass

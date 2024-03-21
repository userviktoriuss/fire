from tkinter.constants import END

import Back.AutoCadFacade as acf
import customtkinter as ctk
import ttkbootstrap as btrp

from Front.Settings import GRAY


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
        super().__init__(master)

        text = '-= Описание =-\n' + text_info.description + '\n' + \
               '-= Параметры =-\n' + text_info.params + '\n' + \
               '-= Рекомендованные значения =-\n' + text_info.recommended_values + '\n' + \
               '-= Примечание =-\n' + text_info.notes
        self.insert(END, text)
        self.configure(state='disabled')


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

        self.left_part_frame = ctk.CTkFrame(self, bg_color='white', fg_color='white')  # ну вот ему пофиг просто
        self.left_panel = ctk.CTkFrame(self.left_part_frame, fg_color=GRAY, border_color='blue', background_corner_colors=('white', 'white', 'white', 'white'))
        self.fill_left_panel_()
        self.right_part_frame = DescriptionFrame(self, self.text_info)

        self.run_button = btrp.Button(self.left_part_frame, text='Запустить алгоритм.', command=self.run_alg_)

        self.left_panel.pack(expand=True, side='top', fill='both')
        self.run_button.pack(side='bottom')

        self.columnconfigure((0, 1), weight=1, uniform='a')
        self.rowconfigure(0, weight=1)
        self.left_part_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        self.right_part_frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        #self.left_part_frame.pack(expand=True, side='left', fill='both', padx=5, pady=5)
        #self.right_part_frame.pack(expand=True, side='right', fill='both', padx=5, pady=5)

    def fill_left_panel_(self):
        pass

    def run_alg_(self):
        pass

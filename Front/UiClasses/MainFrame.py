from enum import Enum
from tkinter import ttk

from Back.AutoCadFacade import AutoCadFacade


class MainFrameMessages:
    NO_CONNECTED_DOCUMENT = 'Нет подключённого документа'
    CONNECTED_TO = 'Подключено к документу {0}'


class MainFrame(ttk.Frame):
    def __init__(self, master, autocad: AutoCadFacade):
        super().__init__(master)
        self.master = master
        self.autocad = autocad

        self.setup_ui()

    def setup_ui(self):
        # Зададим сетку.
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=2)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Создадим и настроим виджеты.
        self.connection_label = ttk.Label(self, text=MainFrameMessages.NO_CONNECTED_DOCUMENT)
        self.connect_button = ttk.Button(self, text='Подключиться', command=self.connect_)

        # Разместим виджеты.
        self.connection_label.grid(row=0, column=0, sticky='e', padx=5)
        self.connect_button.grid(row=0, column=1, sticky='w', padx=5)
        # TODO: настроить виджеты

    def connect_(self):
        drawing = self.autocad.connect()  # TODO: навернуть проверку, кинуть месседж боксы
        self.connection_label['text'] = MainFrameMessages.CONNECTED_TO.format(drawing)

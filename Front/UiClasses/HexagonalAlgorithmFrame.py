from tkinter import ttk

from Back.AutoCadFacade import AutoCadFacade


class HexagonalAlgorithmFrame(ttk.Frame):
    def __init__(self, master, autocad: AutoCadFacade):
        super().__init__(master)
        self.autocad = autocad

        label = ttk.Label(self, text='Шестиугольная сетка йеп')
        label.pack()
        # TODO: настроить виджеты
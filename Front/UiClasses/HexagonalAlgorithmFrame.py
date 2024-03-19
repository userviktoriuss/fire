import tkinter.ttk as ttk

import Back.AutoCadFacade as acf


class HexagonalAlgorithmFrame(ttk.Frame):
    title = 'Шестиугольная сетка'
    def __init__(self, master, autocad: acf.AutoCadFacade):
        super().__init__(master)
        self.autocad = autocad

        label = ttk.Label(self, text='Шестиугольная сетка йеп')
        label.pack()
        # TODO: настроить виджеты
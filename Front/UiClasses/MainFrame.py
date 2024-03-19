import tkinter.ttk as ttk
import Front.UiClasses.MainWindow as mw


class MainFrameMessages:
    NO_CONNECTED_DOCUMENT = 'Нет подключённого документа'
    CONNECTED_TO = 'Подключено к документу {0}'


class MainFrame(ttk.Frame):
    def __init__(self, master: ttk.Notebook, main_window: 'MainWindow'):
        super().__init__(master)
        self.master = master
        self.main_window = main_window
        # self.autocad = main_window.autocad

        self.setup_ui()

    def setup_ui(self):
        # Зададим сетку.
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=2)
        self.columnconfigure(tuple(range(4)), weight=1)

        # Создадим и настроим виджеты.
        self.connection_label = ttk.Label(
            self,
            text=MainFrameMessages.NO_CONNECTED_DOCUMENT,
            justify='center')
        self.connect_button = ttk.Button(self, text='Подключиться', command=self.connect_)

        algs_count = len(self.main_window.algs)
        self.algs_buttons = []

        for i in range(algs_count):
           self.algs_buttons.append(
               # Замыкания берутся по имени переменной, а не по значению/
               # Зафиксируем значение таким способом.
               ttk.Button(self, command=lambda i=i: self.master.select(i + 1))
           )

        # Разместим виджеты.
        self.connection_label.grid(row=0, column=1, columnspan=2, sticky='news')
        self.connect_button.grid(row=0, column=3, sticky='w')

        for i in range(2):
           for j in range(2):
               self.algs_buttons[2 * i + j]\
                   .grid(row=1+i, column=j * 2, columnspan=2, sticky='news')
        # TODO: настроить виджеты

    def connect_(self):
        drawing = self.main_window.autocad.connect()  # TODO: навернуть проверку, кинуть месседж боксы
        self.connection_label['text'] = MainFrameMessages.CONNECTED_TO.format(drawing)

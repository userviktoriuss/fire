import tkinter.ttk as ttk
import tkinter as tk
import Front.UiClasses.MainWindow as mw
from Front.Settings import ColorScheme


class MainFrameMessages:
    NO_CONNECTED_DOCUMENT = 'Нет подключённого документа'
    CONNECTED_TO = 'Подключено к документу {0}'


class MainFrame(ttk.Frame):
    def __init__(self, master: ttk.Notebook, main_window: 'MainWindow'):
        super().__init__(master)
        self.master = master
        self.main_window = main_window

        self.setup_ui()

    def setup_ui(self):
        # Создадим и настроим виджеты. -------------------------------------------
        self.connection_label = ttk.Label(
            self,
            text=MainFrameMessages.NO_CONNECTED_DOCUMENT,
            anchor='center',
            width=70
        )
        self.connect_button = ttk.Button(
            self,
            text='Подключиться',
            command=self.connect_,
            # background=ColorScheme.BG_DARK_COLOR,
            # activebackground=ColorScheme.BG_DARK_COLOR,
            # foreground=ColorScheme.FG_COLOR,
            # activeforeground=ColorScheme.FG_DARK_COLOR,
            # highlightbackground=ColorScheme.BG_DARK_COLOR,
        )

        algs_count = len(self.main_window.algs)
        self.algs_buttons = []

        self.imgs = [
            tk.PhotoImage(file='pics/hexagonal.png'),
            tk.PhotoImage(file='pics/hexagonal.png'),
            tk.PhotoImage(file='pics/hexagonal.png'),
            tk.PhotoImage(file='pics/hexagonal.png')
        ]

        self.hover_imgs = [
            tk.PhotoImage(file='pics/hexagonal_mouse_over.png'),
            tk.PhotoImage(file='pics/hexagonal_mouse_over.png'),
            tk.PhotoImage(file='pics/hexagonal_mouse_over.png'),
            tk.PhotoImage(file='pics/hexagonal_mouse_over.png')
        ]

        tk.PhotoImage()
        for i in range(algs_count):
            # Замыкания берутся по имени переменной, а не по значению/
            # Зафиксируем значение таким способом.
            btn = ttk.Button(self,
                           command=lambda i=i: self.master.select(i + 1),
                           image=self.imgs[i])
            btn.bind('<Enter>', lambda e, i=i: self.enter_(i, e))
            btn.bind('<Leave>', lambda e, i=i: self.leave_(i, e))
            self.algs_buttons.append(btn)


        # Разместим виджеты.
        self.connection_label.place(relx=0.2, rely=0.1)
        self.connect_button.place(relx=0.7, rely=0.1)

        for i in range(2):
            for j in range(2):
                self.algs_buttons[2 * i + j] \
                    .place(relx=0.5 * j, rely=0.2 + 0.4 * i, relheight=0.4, relwidth=0.5)

    def enter_(self, i, event):
        self.algs_buttons[i]['image'] = self.hover_imgs[i]

    def leave_(self, i, event):
        self.algs_buttons[i]['image'] = self.imgs[i]

    def connect_(self):
        drawing = self.main_window.autocad.connect()  # TODO: навернуть проверку, кинуть месседж боксы
        self.connection_label['text'] = MainFrameMessages.CONNECTED_TO.format(drawing)


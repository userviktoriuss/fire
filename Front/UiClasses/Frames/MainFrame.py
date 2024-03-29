import ttkbootstrap as btrp
import customtkinter as ctk
from PIL import Image
from CTkMessagebox import CTkMessagebox
from Front.Utils.Fonts import Fonts
from Front.Settings import HEX, HEX_SIZE, GENETIC, GENETIC_SIZE, RK, RK_SIZE, QUASI, QUASI_SIZE, HEX_HOVERED, \
    GENETIC_HOVERED, RK_HOVERED, QUASI_HOVERED
import logging

logger = logging.getLogger(__name__)


class MainFrameMessages:
    NO_CONNECTED_DOCUMENT = 'Документ не подключен'
    CONNECTED_TO = 'Подключено к {0}'


class MainFrame(ctk.CTkFrame):
    def __init__(self, master: btrp.Notebook, main_window: 'MainWindow'):
        super().__init__(master)
        self.master = master
        self.main_window = main_window

        self.setup_ui()

    def setup_ui(self):
        # Создадим и настроим виджеты. -------------------------------------------
        self.connection_label = ctk.CTkLabel(
            self,
            text=MainFrameMessages.NO_CONNECTED_DOCUMENT,
            anchor='center',
            width=70,
            font=Fonts.connection_font
        )
        self.connect_button = ctk.CTkButton(
            self,
            text='Подключиться',
            command=self.connect_,
            font=Fonts.button_font
        )

        # Кнопки для алгоритмов -------------------------------------------------------------
        algs_count = len(self.main_window.algs)
        self.algs_buttons = []

        self.imgs = [
            ctk.CTkImage(dark_image=Image.open(HEX), size=HEX_SIZE),
            ctk.CTkImage(dark_image=Image.open(GENETIC), size=GENETIC_SIZE),
            ctk.CTkImage(dark_image=Image.open(RK), size=RK_SIZE),
            ctk.CTkImage(dark_image=Image.open(QUASI), size=QUASI_SIZE)
        ]

        self.hover_imgs = [
            ctk.CTkImage(dark_image=Image.open(HEX_HOVERED), size=HEX_SIZE),
            ctk.CTkImage(dark_image=Image.open(GENETIC_HOVERED), size=GENETIC_SIZE),
            ctk.CTkImage(dark_image=Image.open(RK_HOVERED), size=RK_SIZE),
            ctk.CTkImage(dark_image=Image.open(QUASI_HOVERED), size=QUASI_SIZE)
        ]

        for i in range(algs_count):
            # Замыкания берутся по имени переменной, а не по значению/
            # Зафиксируем значение таким способом.
            btn = ctk.CTkButton(self,
                                text='',
                                command=lambda i=i: self.master.select(i + 1),
                                image=self.imgs[i],
                                bg_color='transparent',
                                fg_color='transparent'
                                )
            btn.bind('<Enter>', lambda e, i=i: self.enter_(i, e))
            btn.bind('<Leave>', lambda e, i=i: self.leave_(i, e))
            self.algs_buttons.append(btn)

        # Разместим виджеты --------------------------------------------------------------
        self.connection_label.place(relx=0.42, rely=0.1)
        self.connect_button.place(relx=0.7, rely=0.1)

        # TODO: сделать grid, добавить параметр auto
        for i in range(2):
            for j in range(2):
                self.algs_buttons[2 * i + j] \
                    .place(relx=0.5 * j, rely=0.2 + 0.4 * i, relheight=0.4, relwidth=0.5)

        logger.debug('UI set-upped successfully')

    def enter_(self, i, event):
        self.algs_buttons[i].configure(
            image=self.hover_imgs[i],
            bg_color='transparent',
            fg_color='transparent')

    def leave_(self, i, event):
        self.algs_buttons[i].configure(
            image=self.imgs[i],
            bg_color='transparent',
            fg_color='transparent')

    def connect_(self):
        try:
            drawing = self.main_window.autocad.connect()
            self.connection_label.configure(text=MainFrameMessages.CONNECTED_TO.format(drawing))
            logger.info('Connected to AutoCAD')
        except Exception as e:
            logger.error('Can\'t connect to AutoCAD: %s', str(e))
            CTkMessagebox(title='Ошибка!',
                          message='Не удалось подключиться к чертежу. \n' + \
                                  'Запустите AutoCAD или прервите в нём все активные команды.',
                          icon='cancel',
                          width=580,
                          font=Fonts.text_font)

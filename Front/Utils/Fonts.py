import customtkinter as ctk
from Settings import *


class Fonts:
    """
    Этот класс хранит набор шрифтов, используемых всеми виджетами.
    """
    text_font = None
    header_font = None
    connection_font = None
    button_font = None
    label_font = None

    @classmethod
    def setup_fonts(cls):
        cls.text_font = ctk.CTkFont(family=FONT, size=TEXT_SIZE)
        cls.header_font = ctk.CTkFont(family=FONT, size=HEADER_SIZE, weight='bold')
        cls.connection_font = ctk.CTkFont(family=FONT, size=CONNECTION_TEXT_SIZE, weight='bold')
        cls.button_font = ctk.CTkFont(family=FONT, size=BUTTON_TEXT_SIZE)
        cls.label_font = ctk.CTkFont(family=FONT, size=LABEL_TEXT_SIZE)

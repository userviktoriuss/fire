from CTkMessagebox import CTkMessagebox

from Front.Utils.Fonts import Fonts
from Front.Settings import ICON


class MsgBox:
    """
    Содержит методы для вызова сообщений типа MessageBox в едином стиле.
    """

    @staticmethod
    def show_error_msgbox(text, title='Ошибка!'):
        CTkMessagebox(title=title,
                      message=text,
                      icon='cancel',
                      width=580,
                      font=Fonts.text_font)

    @staticmethod
    def show_info_msgbox(text, title=''):
        CTkMessagebox(title=title,
                      message=text,
                      icon='info',
                      width=580,
                      font=Fonts.text_font)

    @staticmethod
    def show_about_program_msgbox_():
        CTkMessagebox(title='О программе',
                      message='-= Дополнение для AutoCAD =-\n\n' + \
                              'Версия 1.0\n\n' + \
                              'Филимонов Виктор, 2024',
                      icon=ICON,
                      width=580,
                      font=Fonts.text_font)

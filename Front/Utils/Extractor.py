from CTkMessagebox import CTkMessagebox

from Front.Utils.Fonts import Fonts


class Exctractor:
    @staticmethod
    def get(type_: 'type to cast to', text: str, param_name: str):
        try:
            return type_(text)
        except:
            CTkMessagebox(title='Ошибка!',
                          message=f'Не удалось привести параметр {param_name} с значением {text} к типу {str(type_)}. \n' + \
                                  'Исправьте значение.',
                          icon='cancel',
                          width=580,
                          font=Fonts.text_font)
            raise
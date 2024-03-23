from CTkMessagebox import CTkMessagebox

from Front.Fonts import Fonts


class Exctractor:
    @staticmethod
    def get_float(text: str, param_name: str) -> float:
        return Exctractor.get(float, text, param_name)

    @staticmethod
    def get_int(text: str, param_name: str) -> int:
        return Exctractor.get(int, text, param_name)

    @staticmethod
    def get(type: 'type to cast to', text: str, param_name: str):
        try:
            return type(text)
        except:
            CTkMessagebox(title='Ошибка!',
                          message=f'Не удалось привести параметр {param_name} с значением {text} к типу {str(type)}. \n' + \
                                  'Исправьте значение.',
                          icon='cancel',
                          width=580,
                          font=Fonts.text_font)
            raise
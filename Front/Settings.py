import tkinter.ttk as ttk
# Шрифты
FONT = 'Calibri'
MAIN_TEXT_SIZE = 150
INPUT_FONT_SIZE = 26
SWITCH_FONT_SIZE = 18

# Цвета
BLUE = '#454f61'
LIGHT_BLUE = '#535d6f'
DARK_BLUE = '#222933'
LIGHT_DARK_BLUE = '#303741'
GRAY = '#727781'
WHITE = '#f5f5f5'
DARK_WHITE = '#bbbcbf'


# icon by <a href="https://www.flaticon.com/free-icons/fire" title="fire icons">Fire icons created by Freepik - Flaticon</a>
ICON = 'pics/fire.ico'


"""
class ColorScheme:
    @staticmethod
    def configure_colors():
        dark_theme = {
            '.': {
                'configure': {
                    'font': ("Colibri", 14),
                    'background': ColorScheme.BG_COLOR,  # Dark grey background
                    'foreground': ColorScheme.FG_COLOR,  # White text TODO: Другой
                }
            },
            'TLabel': {
                'configure': {
                    'foreground': ColorScheme.FG_COLOR,  # White text
                }
            },
            'TButton': {
                'map': {
                    'background': [('active', 'pressed', ColorScheme.BG_DARK_PRESSED_COLOR),
                                   ('!disabled', ColorScheme.BG_DARK_COLOR)],  # Dark blue-grey button
                    'foreground': [('active', 'pressed', ColorScheme.FG_COLOR),
                                   ('!disabled', ColorScheme.FG_COLOR)],  # White text
                }
            },
        }
        style = ttk.Style()

        style.theme_create('dark', parent='clam', settings=dark_theme)
        style.theme_use('dark')
"""
import tkinter.ttk as ttk


class ColorScheme:
    BG_COLOR = '#454f61'
    BG_DARK_COLOR = '#222933'
    BG_DARK_PRESSED_COLOR = '#303741'
    LIGHT_COLOR = '#727781'
    FG_COLOR = '#f5f5f5'
    FG_DARK_COLOR = '#bbbcbf'

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

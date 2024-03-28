from Front.Settings import LOGGING_CONF
from Front.UiClasses.CantLoadWindow import CantLoadWindow
from Front.UiClasses.MainWindow import MainWindow
from ctypes import windll
import logging.config


if __name__ == '__main__':
    try:
        # Подключим логирование.
        logging.config.fileConfig(LOGGING_CONF)
        # Создадим окно.
        window = MainWindow('Дополнение для AutoCAD', '1280x720')
    except Exception as e:
        print(e)
        # Создадим окно с сообщением о критической ошибке
        window = CantLoadWindow('Дополнение для AutoCAD', '320x130')

    # Избавимся от размытости текста.
    windll.shcore.SetProcessDpiAwareness(1)

    # Запустим приложение.
    window.mainloop()

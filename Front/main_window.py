from Front.Settings import LOGGING_PATH
from Front.UiClasses.MainWindows.CantLoadWindow import CantLoadWindow
from Front.UiClasses.MainWindows.MainWindow import MainWindow
from ctypes import windll
import logging.config

# Это корневой файл программы.
# Его следует запускать, чтобы начать работу.


if __name__ == '__main__':
    try:
        # Подключим логирование.
        logging.basicConfig(
            filename=LOGGING_PATH,
            level=logging.INFO
        )
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

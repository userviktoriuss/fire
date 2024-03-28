from Front.UiClasses.MainWindow import MainWindow
from ctypes import windll
import logging.config

#logging.config.fileConfig(LOGGING_CONF)

# Создадим окно.
window = MainWindow('Дополнение для AutoCAD', '1280x720')

# Избавимся от размытости текста.
windll.shcore.SetProcessDpiAwareness(1)

# Запустим приложение.
window.mainloop()
exit(0)

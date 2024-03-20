from Front.UiClasses.MainWindow import MainWindow
from ctypes import windll

# Создадим окно.
window = MainWindow('Дополнение для AutoCAD', '1280x720')

# Избавимся от размытости текста.
windll.shcore.SetProcessDpiAwareness(1)

#ColorScheme.configure_colors()

# Запустим приложение.
window.mainloop()
exit(0)

from tkinter import ttk
from Front.UiClasses.MainWindow import MainWindow

# Создадим окно.
window = MainWindow('Дополнение для AutoCAD', '1280x720')

# Запустим приложение.
window.mainloop()
exit(0)

# ---------------------------------------------------------------------------
# Добавим виджеты.
label1 = ttk.Label(window, text='label1', background='red')
label2 = ttk.Label(window, text='label2', background='blue')

# Расставим все виджеты на свои места.
#pack
#label1.pack(side='left', fill='both', expand=True)
#label2.pack(side='right', fill='both', expand=True)

#grid
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=2)

window.rowconfigure(0, weight=1)

label1.grid(row=0, column=1, sticky='nesw')
label2.grid(row=0, column=2, sticky='nswe')

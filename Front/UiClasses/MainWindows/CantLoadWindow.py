import customtkinter as ctk


class CantLoadWindow(ctk.CTk):
    """
    Это окно отображается, когда вследствие критической ошибки не удалось создать основное окно.
    """

    def __init__(self, title, geometry):
        super().__init__()
        self.title(title)
        self.geometry(geometry)

        self.label = ctk.CTkLabel(
            self,
            wraplength=300,
            text='Произошла критическая ошибка, не давшая загрузить окно приложения.\nОна могла возникнуть из-за нарушения целостности программы или некорректного формата настроек.\nПожалуйста, проверьте корректность настроек по умолчанию или переустановите программу.',
            justify='left')
        self.label.pack(fill='both', padx=10, pady=10)

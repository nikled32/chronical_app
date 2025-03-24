import flet as ft

def IndexView(page: ft.Page):
    # Настройки страницы
    page.title = "Отслеживание хронических заболеваний"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 50

    # Функция для обработки выбора режима
    def select_mode(e):
        if e.control.text == "Я врач":
            page.clean()
            page.add(ft.Text("Режим врача", size=24, weight="bold"))
            # Здесь можно добавить интерфейс врача
        elif e.control.text == "Я пациент":
            page.clean()
            page.add(ft.Text("Режим пациента", size=24, weight="bold"))
            # Здесь можно добавить интерфейс пациента

    # Кнопки для выбора режима
    doctor_button = ft.ElevatedButton(
        text="Я врач",
        on_click=select_mode,
        width=200,
        height=50,
    )

    patient_button = ft.ElevatedButton(
        text="Я пациент",
        on_click=select_mode,
        width=200,
        height=50,
    )

    # Добавление элементов на страницу
    page.add(
        ft.Column(
            [
                ft.Text("Добро пожаловать!", size=24, weight="bold"),
                ft.Text("Выберите режим:", size=18),
                doctor_button,
                patient_button,
            ],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

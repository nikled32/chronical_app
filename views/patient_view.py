import flet as ft


def PatientView(page: ft = ft):

    page.title = "Отслеживание хронических заболеваний"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 50

    # Кнопки для выбора режима
    doctor_button = ft.ElevatedButton(
        text="Я писька?",
        on_click=lambda _: page.go("/patient_page"),
        width=200,
        height=50,
    )

    # Добавление элементов на страницу
    page.add(
        ft.Column(
            [
                ft.Text("Добро пожаловать!", size=24, weight="bold"),
                ft.Text("Ваш режим пациент:", size=18),
            ],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

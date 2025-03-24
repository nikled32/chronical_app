import flet as ft


# Страница пациента
def patient_page(page: ft.Page):
    page.clean()
    page.add(
        ft.Column(
            [
                ft.Text("Режим пациента", size=24, weight="bold"),
                ft.Text("Режим pisyapopa", size=24),
                ft.ElevatedButton(
                    text="На главную",
                    on_click=lambda e: page.go("/"),  # Возврат на главную страницу
                ),
            ],
            spacing=20,
        )
    )
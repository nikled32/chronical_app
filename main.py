import flet as ft
from doctor_page import doctor_page, doctor_patient_page
from patient_page import patient_page


# Главная страница
def main_page(page: ft.Page):
    page.clean()


    page.add(
        ft.Column(
            [
                ft.Text("Добро пожаловать!", size=24, weight="bold"),
                ft.Text("Выберите режим:", size=18),
                ft.ElevatedButton(
                    text="Я врач",
                    on_click=lambda e: page.go("/doctor"),
                    width=200,
                    height=50,
                ),
                ft.ElevatedButton(
                    text="Я пациент",
                    on_click=lambda e: page.go("/patient"),
                    width=200,
                    height=50,
                ),
            ],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

# Основная функция
def main(page: ft.Page):
    # Настройки страницы
    page.title = "Отслеживание хронических заболеваний"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 50

    # Обработка изменения маршрута
    def route_change(e):
        if page.route == "/":
            main_page(page)
        elif page.route == "/doctor":
            doctor_page(page)
        elif page.route.startswith("/doctor/patient/"):  # Обработка страницы пациента врача
            patient_id = page.route.split("/")[-1]  # Извлекаем ID пациента из URL
            doctor_patient_page(page, patient_id)
        elif page.route == "/patient":
            patient_page(page)

    # Обработка начального маршрута
    def on_load(e):
        if page.route == "":
            page.route = "/"
        route_change(None)

    # Подписка на события
    page.on_route_change = route_change
    page.on_load = on_load

    # Загрузка начальной страницы
    on_load(None)


# Запуск приложения
ft.app(target=main)



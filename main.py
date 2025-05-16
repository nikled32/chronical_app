import flet as ft
from doctor_page import doctor_page, doctor_patient_page
from patient_page import patient_page
from db_add_auth import check_credentials


# Главная страница авторизации
def main_page(page: ft.Page):
    page.clean()

    # Элементы интерфейса
    login_field = ft.TextField(label="Логин", width=300)
    password_field = ft.TextField(label="Пароль", password=True, width=300)
    role_selector = ft.Dropdown(
        width=300,
        options=[
            ft.dropdown.Option("doctor", "Я врач"),
            ft.dropdown.Option("patient", "Я пациент"),
        ],
        value="doctor"
    )
    error_text = ft.Text("", color="red")  # Для вывода ошибок

    def login_click(e):
        login = login_field.value
        password = password_field.value
        role = role_selector.value

        if not login or not password:
            error_text.value = "Введите логин и пароль!"
            page.update()
            return

        if check_credentials(login, password, role):
            error_text.value = ""  # Очищаем сообщение об ошибке
            page.session.set("user_role", role)
            page.session.set("user_login", login)

            if role == "doctor":
                page.go("/doctor")
            else:
                page.go("/patient")
        else:
            error_text.value = "Неверный логин или пароль!"
            page.update()

    page.add(
        ft.Column(
            [
                ft.Text("Система отслеживания заболеваний", size=24, weight="bold"),
                ft.Text("Авторизация", size=20),
                login_field,
                password_field,
                role_selector,
                error_text,  # Добавляем элемент для вывода ошибок
                ft.ElevatedButton(
                    text="Войти",
                    on_click=login_click,
                    width=200,
                    height=50,
                ),
            ],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )


# Основная функция (остается без изменений)
def main(page: ft.Page):
    # Настройки страницы
    page.title = "Медицинский мониторинг"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 50

    def route_change(e):
        protected_routes = ["/doctor", "/patient", "/doctor/patient"]
        if any(page.route.startswith(route) for route in protected_routes):
            if not page.session.get("user_login"):
                page.go("/")
                return

        if page.route == "/":
            main_page(page)
        elif page.route == "/doctor":
            doctor_page(page)
        elif page.route.startswith("/doctor/patient/"):
            patient_id = page.route.split("/")[-1]
            doctor_patient_page(page, patient_id)
        elif page.route == "/patient":
            patient_page(page)

    def on_load(e):
        if page.route == "":
            page.route = "/"
        route_change(None)

    page.on_route_change = route_change
    page.on_load = on_load
    on_load(None)


if __name__ == "__main__":
    ft.app(target=main)
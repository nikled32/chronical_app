import flet as ft
import sqlite3
from datetime import datetime
import random


# Функция для вычисления возраста
def calculate_age(date_of_birth):
    """Вычисляет возраст на основе даты рождения."""
    today = datetime.today()
    birth_date = datetime.strptime(date_of_birth, "%Y-%m-%d")
    age = today.year - birth_date.year

    # Корректировка возраста, если день рождения еще не наступил в этом году
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1

    return age


# Функция для получения списка недавних пациентов
def get_recent_patients():
    conn = sqlite3.connect("chronic_diseases.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, name, date_of_birth
        FROM patients
        WHERE last_accessed IS NOT NULL
        ORDER BY last_accessed DESC
        LIMIT 5
    ''')  # Получаем 5 последних пациентов
    patients = cursor.fetchall()
    conn.close()
    return patients


# Функция для получения данных о пациенте
def get_patient_data(patient_id):
    conn = sqlite3.connect("chronic_diseases.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT name, date_of_birth, smoking, alcohol, medical_history
        FROM patients
        WHERE id = ?
    ''', (patient_id,))
    patient_data = cursor.fetchone()
    conn.close()
    return patient_data


# Функция для генерации случайных данных для графиков
def generate_random_data():
    """Генерирует случайные данные для графиков."""
    data = {
        "heart_rate": [random.randint(60, 100) for _ in range(30)],  # ЧСС
        "blood_pressure": [(random.randint(110, 130), random.randint(70, 90)) for _ in range(30)],  # Артериальное давление
        "blood_sugar": [random.randint(70, 120) for _ in range(30)],  # Уровень сахара в крови
    }
    return data


# Функция для получения списка всех пациентов
def get_all_patients():
    conn = sqlite3.connect("chronic_diseases.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, date_of_birth FROM patients ORDER BY name")  # Получаем всех пациентов
    patients = cursor.fetchall()
    conn.close()
    return patients


# Функция для создания интерфейса врача
def doctor_page(page: ft.Page):
    page.clean()

    # Заголовок страницы
    title = ft.Text("Режим врача", size=24, weight="bold")

    # Секция "Недавние пациенты" (таблица)
    recent_patients_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Имя пациента", weight="bold")),
            ft.DataColumn(ft.Text("Возраст", weight="bold")),  # Новый столбец для возраста
            ft.DataColumn(ft.Text("Дата рождения", weight="bold")),  # Новый столбец для даты рождения
        ],
        rows=[],
    )

    # Заполнение таблицы недавних пациентов
    def load_recent_patients():
        recent_patients = get_recent_patients()
        recent_patients_table.rows.clear()
        for patient in recent_patients:
            patient_id, patient_name, date_of_birth = patient
            age = calculate_age(date_of_birth)  # Вычисляем возраст
            recent_patients_table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Text(patient_name, size=16),
                            on_tap=lambda e, id=patient_id: select_patient(id),  # Передаем ID пациента
                        ),
                        ft.DataCell(ft.Text(f"{age} лет", size=16)),  # Отображаем возраст
                        ft.DataCell(ft.Text(date_of_birth, size=16)),  # Отображаем дату рождения
                    ],
                )
            )
        page.update()  # Обновляем страницу после изменения таблицы

    # Секция "Все пациенты" (ListView с поиском)
    all_patients_list = ft.ListView(expand=True, spacing=10)

    # Поле поиска
    search_field = ft.TextField(
        hint_text="Поиск по имени",
        on_change=lambda e: filter_patients(),  # Фильтрация при изменении текста
        #width=300,
    )

    # Заполнение списка всех пациентов
    def load_all_patients():
        all_patients = get_all_patients()
        all_patients_list.controls.clear()
        for patient in all_patients:
            patient_id, patient_name, date_of_birth = patient
            age = calculate_age(date_of_birth)  # Вычисляем возраст
            all_patients_list.controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(patient_name, size=16),
                            ft.Text(f"Возраст: {age} лет", size=14),  # Отображаем возраст
                            ft.Text(f"Дата рождения: {date_of_birth}", size=14),  # Отображаем дату рождения
                        ],
                        spacing=5,
                    ),
                    padding=10,
                    bgcolor=ft.colors.BLUE_100,
                    border_radius=10,
                    on_click=lambda e, id=patient_id: select_patient(id),  # Передаем ID пациента
                )
            )
        page.update()  # Обновляем страницу после изменения списка

    # Функция для фильтрации пациентов по имени
    def filter_patients():
        search_query = search_field.value.lower()
        all_patients = get_all_patients()
        all_patients_list.controls.clear()
        for patient in all_patients:
            patient_id, patient_name, date_of_birth = patient
            if search_query in patient_name.lower():
                age = calculate_age(date_of_birth)  # Вычисляем возраст
                all_patients_list.controls.append(
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(patient_name, size=16),
                                ft.Text(f"Возраст: {age} лет", size=14),  # Отображаем возраст
                                ft.Text(f"Дата рождения: {date_of_birth}", size=14),  # Отображаем дату рождения
                            ],
                            spacing=5,
                        ),
                        padding=10,
                        bgcolor=ft.colors.BLUE_100,
                        border_radius=10,
                        on_click=lambda e, id=patient_id: select_patient(id),  # Передаем ID пациента
                    )
                )
        page.update()  # Обновляем страницу после изменения списка

    # Функция для выбора пациента
    def select_patient(patient_id):
        page.go(f"/doctor/patient/{patient_id}")  # Переход на страницу пациента

    # Кнопка "На главную"
    home_button = ft.ElevatedButton(
        text="На главную",
        on_click=lambda e: page.go("/"),
    )

    # Основной интерфейс
    page.add(
        ft.Column(
            [
                title,
                ft.Container(
                    content=ft.Row(
                        [
                            # Левая колонка: Недавние пациенты
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Text("Недавние пациенты:", size=18, weight="bold"),
                                        ft.Container(
                                            content=recent_patients_table,
                                            padding=10,
                                            border=ft.border.all(1, ft.colors.GREY_400),
                                            border_radius=10,
                                            width=500,  # Фиксированная ширина для левой колонки
                                        ),
                                    ],
                                    spacing=10,
                                ),
                                padding=10,
                            ),
                            # Правая колонка: Все пациенты
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Text("Все пациенты:", size=18, weight="bold"),
                                        search_field,  # Поле поиска
                                        ft.Container(
                                            content=all_patients_list,
                                            height=400,  # Фиксированная высота для прокрутки
                                            padding=10,
                                            border=ft.border.all(1, ft.colors.GREY_400),
                                            border_radius=10,
                                            #width=400,  # Фиксированная ширина для правой колонки
                                            expand=True,  # Растягиваем контейнер на доступное пространство
                                        ),
                                    ],
                                    spacing=10,
                                ),
                                padding=10,
                                expand=True,  # Растягиваем правую колонку на всё доступное пространство
                            ),
                        ],
                        spacing=20,  # Расстояние между колонками
                        alignment=ft.MainAxisAlignment.CENTER,  # Выравниваем колонки по центру
                    ),
                    alignment=ft.alignment.center,  # Центрируем контейнер по центру страницы
                ),
                home_button,
            ],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,  # Растягиваем колонку на всю доступную высоту
        )
    )

    # Загрузка недавних пациентов при открытии страницы
    load_recent_patients()

    # Загрузка всех пациентов при открытии страницы
    load_all_patients()


# Функция для создания страницы пациента
def doctor_patient_page(page: ft.Page, patient_id: int):
    # Обновляем поле last_accessed текущей датой и временем
    conn = sqlite3.connect("chronic_diseases.db")
    cursor = conn.cursor()
    cursor.execute('''
            UPDATE patients SET last_accessed = ? WHERE id = ?
        ''', (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), patient_id))
    conn.commit()

    cursor.execute('''
            SELECT name, date_of_birth, smoking, alcohol, medical_history 
            FROM patients WHERE id = ?
        ''', (patient_id,))
    patient_data = cursor.fetchone()
    conn.close()

    if not patient_data:
        page.add(ft.Text("Пациент не найден", size=24, weight="bold"))
        return

    name, date_of_birth, smoking, alcohol, medical_history = patient_data
    age = calculate_age(date_of_birth)



    # Генерация случайных данных для графиков
    data = generate_random_data()

    # Левая колонка - информация о пациенте
    info_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Параметр", weight="bold")),
            ft.DataColumn(ft.Text("Значение", weight="bold")),
        ],
        rows=[
            ft.DataRow(cells=[
                ft.DataCell(ft.Text("ФИО:", size=16)),
                ft.DataCell(ft.Text(name, size=16)),
            ]),
            ft.DataRow(cells=[
                ft.DataCell(ft.Text("Возраст:", size=16)),
                ft.DataCell(ft.Text(f"{age} лет", size=16)),
            ]),
            ft.DataRow(cells=[
                ft.DataCell(ft.Text("Курение:", size=16)),
                ft.DataCell(ft.Text("Да" if smoking else "Нет", size=16)),
            ]),
            ft.DataRow(cells=[
                ft.DataCell(ft.Text("Алкоголь:", size=16)),
                ft.DataCell(ft.Text("Да" if alcohol else "Нет", size=16)),
            ]),
            ft.DataRow(cells=[
                ft.DataCell(ft.Text("История болезней:", size=16)),
                ft.DataCell(ft.Text(medical_history if medical_history else "Нет данных", size=16)),
            ]),
            ft.DataRow(cells=[
                ft.DataCell(ft.Text("Текущие симптомы:", size=16)),
                ft.DataCell(ft.Text("Головная боль, усталость", size=16)),
            ]),
        ],
    )

    # Правая колонка - графики с возможностью скроллинга
    def create_chart(data, title, y_label, x_label="Дни наблюдения"):
        # Автоматическое определение подходящего шага для значений оси Y
        data_range = max(data) - min(data) if data else 1
        y_step = max(1, round(data_range / 5))  # Всегда минимум 1 и около 5 делений

        return ft.Container(
            content=ft.Column([
                ft.Text(title, size=16, weight="bold"),
                ft.Row([
                    # Подпись оси Y
                    ft.Container(
                        ft.Text(y_label, size=12, color=ft.colors.GREY, rotate=0),
                        width=40,
                        alignment=ft.alignment.center
                    ),
                    # Сам график
                    ft.Container(
                        ft.LineChart(
                            data_series=[
                                ft.LineChartData(
                                    data_points=[ft.LineChartDataPoint(i, value) for i, value in enumerate(data)],
                                    stroke_width=3,
                                    color=ft.colors.BLUE,
                                    curved=True,
                                ),
                            ],
                            border=ft.border.all(1, ft.colors.GREY_300),
                            left_axis=ft.ChartAxis(
                                labels=[
                                    ft.ChartAxisLabel(
                                        value=min(data) + i * y_step,
                                        label=ft.Text(str(round(min(data) + i * y_step, 1)), size=10),
                                    )
                                    for i in range(6) if len(data) > 0
                                ],
                                labels_size=40,
                            ),
                            bottom_axis=ft.ChartAxis(
                                labels=[
                                    ft.ChartAxisLabel(
                                        value=i,
                                        label=ft.Text(str(i + 1), size=10),
                                    )
                                    for i in range(0, len(data), max(1, len(data) // 5)) if len(data) > 0
                                ],
                                labels_size=40,
                            ),
                            min_y=max(0, (min(data) if data else 0) - 0.1 * data_range),
                            max_y=(max(data) if data else 10) + 0.1 * data_range,
                        ),
                        expand=True,
                    )
                ], spacing=5, expand=True),
                # Подпись оси X
                ft.Container(
                    ft.Text(x_label, size=12, color=ft.colors.GREY),
                    padding=ft.padding.only(top=10),
                    alignment=ft.alignment.center
                )
            ], spacing=5),
            padding=10,
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=10,
            height=250,
            expand=True
        )

    # Контейнер с графиками
    charts_column = ft.Column([
        create_chart(data["heart_rate"], "Частота сердечных сокращений", "уд/мин"),
        create_chart([systolic for systolic, _ in data["blood_pressure"]], "Артериальное давление", "мм рт.ст."),
        create_chart(data["blood_sugar"], "Уровень сахара в крови", "мг/дл"),
    ], spacing=20)

    scrollable_charts = ft.Container(
        content=ft.ListView(
            controls=[charts_column],
            expand=True,
            spacing=20,
            padding=10,
        ),
        expand=True,
    )

    def open_medical_history_form(patient_id):
        """Открывает форму для добавления записи в историю болезни."""
        new_note_field = ft.TextField(
            multiline=True,
            min_lines=3,
            hint_text="Введите новую запись (симптомы, диагноз, рекомендации)...",
            width=500,
        )


        def save_note(e):
            if not new_note_field.value.strip():
                return  # Не сохраняем пустые записи

            # Обновляем БД
            conn = sqlite3.connect("chronic_diseases.db")
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE patients 
                SET medical_history = COALESCE(medical_history || '\n', '') || ?
                WHERE id = ?
            ''', (f"{datetime.now().strftime('%Y-%m-%d')}: {new_note_field.value}", patient_id))
            conn.commit()
            conn.close()

            # Закрываем диалог и обновляем страницу
            close_dialog()
            doctor_patient_page(page, patient_id)  # Перезагружаем страницу

        page.dialog = ft.AlertDialog(
            title=ft.Text("Добавить запись в историю болезни"),
            content=new_note_field,
            actions=[
                ft.TextButton("Отмена", on_click=lambda e: close_dialog()),
                ft.TextButton("Сохранить", on_click=save_note),
            ],
        )
        page.dialog.open = True
        page.update()


    def show_contact_dialog(patient_name):
        """Показывает контакты пациента в диалоговом окне."""
        # Заглушка: в реальном приложении эти данные можно брать из БД
        contact_info = {
            "Телефон": "+7 (XXX) XXX-XX-XX",  # Пример, можно добавить поле в БД
            "Email": "patient@example.com",  # Пример
            "Адрес": "г. Москва, ул. Примерная, 123",
        }

        # Создаем содержимое диалога
        dialog_content = ft.Column([
            ft.Text(f"Контактные данные пациента {patient_name}:", size=18),
            *[
                ft.Text(f"{key}: {value}", size=16)
                for key, value in contact_info.items()
            ],
        ], tight=True)

        # Показываем диалог
        page.dialog = ft.AlertDialog(
            title=ft.Text("Контакты"),
            content=dialog_content,
            actions=[ft.TextButton("Закрыть", on_click=lambda e: close_dialog())],
        )
        page.dialog.open = True
        page.update()

    def close_dialog():
        page.dialog.open = False
        page.update()

    # --- Создаем кнопки ---
    action_buttons = ft.Row(
        [
            ft.ElevatedButton(
                text="Назад к списку",
                on_click=lambda e: page.go("/doctor"),
                width=200,
                height=40,
            ),
            ft.ElevatedButton(
                text="Связаться с пациентом",
                on_click=lambda e: show_contact_dialog(name),
                width=200,
                height=40,
                icon=ft.icons.CONTACT_PHONE,
            ),
            ft.ElevatedButton(
                text="Добавить запись",
                on_click=lambda e: open_medical_history_form(patient_id),
                width=200,
                height=40,
                icon=ft.icons.ADD_CIRCLE_OUTLINE,
            ),
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # Основной интерфейс
    page.clean()
    page.add(
        ft.Column(
            controls=[
                # 1. Заголовок с именем и ID
                ft.Text(f"Карта пациента: {name} (ID: {patient_id})", size=24, weight="bold"),

                # 2. Основной контент (инфо + графики)
                ft.Row(
                    controls=[
                        # Левая колонка — информация о пациенте
                        ft.Container(
                            content=info_table,
                            width=350,
                            padding=20,
                            border=ft.border.all(1, ft.colors.GREY_300),
                            border_radius=10,
                        ),

                        # Правая колонка — графики
                        ft.Container(
                            content=scrollable_charts,
                            expand=True,
                            padding=10,
                        ),
                    ],
                    expand=True,
                    spacing=20,
                ),

                # 3. Кнопки действий
                action_buttons,
            ],
            expand=True,
            spacing=20,
        )
    )
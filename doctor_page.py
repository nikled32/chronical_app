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
# def generate_random_data():
#     """Генерирует случайные данные для графиков."""
#     data = {
#         "heart_rate": [random.randint(60, 100) for _ in range(30)],  # ЧСС
#         "blood_pressure": [(random.randint(110, 130), random.randint(70, 90)) for _ in range(30)],  # Артериальное давление
#         "blood_sugar": [random.randint(70, 120) for _ in range(30)],  # Уровень сахара в крови
#     }
#     return data


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


def get_heart_rate_data(patient_id):
    conn = sqlite3.connect("chronic_diseases.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT measurement_time, rate
        FROM heart_rates
        WHERE patient_id = ?
        ORDER BY measurement_time
    """, (patient_id,))
    data = cursor.fetchall()
    conn.close()
    return [(row[0], row[1]) for row in data]


def get_blood_pressure_data(patient_id):
    conn = sqlite3.connect("chronic_diseases.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT measurement_time, systolic, diastolic
        FROM blood_pressure
        WHERE patient_id = ?
        ORDER BY measurement_time
    """, (patient_id,))
    data = cursor.fetchall()
    conn.close()
    return [(row[0], row[1], row[2]) for row in data]


def get_blood_sugar_data(patient_id):
    conn = sqlite3.connect("chronic_diseases.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT measurement_time, level
        FROM blood_sugar
        WHERE patient_id = ?
        ORDER BY measurement_time
    """, (patient_id,))
    data = cursor.fetchall()
    conn.close()
    return [(row[0], row[1]) for row in data]


# Функция для создания страницы пациента
def doctor_patient_page(page: ft.Page, patient_id: int):
    # Обновляем поле last_accessed текущей датой и временем
    conn = sqlite3.connect("chronic_diseases.db")
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE patients SET last_accessed = ? WHERE id = ?
    ''', (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), patient_id))
    conn.commit()

    # Получаем данные о пациенте
    cursor.execute('''
        SELECT name, date_of_birth, smoking, alcohol, medical_history, contact_info
        FROM patients WHERE id = ?
    ''', (patient_id,))
    patient_data = cursor.fetchone()
    conn.close()

    if not patient_data:
        page.add(ft.Text("Пациент не найден", size=24, weight="bold"))
        return

    name, date_of_birth, smoking, alcohol, medical_history, contact_info = patient_data
    age = calculate_age(date_of_birth)

    # --- Загрузка реальных данных из БД ---
    heart_rate_raw = get_heart_rate_data(patient_id)
    blood_pressure_raw = get_blood_pressure_data(patient_id)
    blood_sugar_raw = get_blood_sugar_data(patient_id)

    # --- Подготовка данных для графиков ---
    heart_rate_values = [rate for _, rate in heart_rate_raw]
    blood_pressure_values = [(systolic, diastolic) for _, systolic, diastolic in blood_pressure_raw]
    blood_sugar_values = [level for _, level in blood_sugar_raw]

    data = {
        "heart_rate": heart_rate_values,
        "blood_pressure": blood_pressure_values,
        "blood_sugar": blood_sugar_values,
    }

    # Создаем элементы диалогов заранее
    # Создаем элементы диалогов заранее
    data_fields = [
        ft.TextField(label="Систолическое давление", hint_text="Напр. 120", width=200),
        ft.TextField(label="Диастолическое давление", hint_text="Напр. 80", width=200),
        ft.TextField(label="Пульс", hint_text="Напр. 70", width=200),
        ft.TextField(label="Сахар в крови", hint_text="Напр. 3.3", width=200)
    ]

    new_note_field = ft.TextField(
        multiline=True,
        min_lines=3,
        hint_text="Введите новую запись...",
        width=400
    )

    contact_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Контактные данные"),
        content=ft.Column([
            ft.Text(f"Пациент: {name}", size=18),
            ft.Divider(),
            ft.Text(f"Email: {contact_info}"),
            ft.Text("Адрес: г. Москва, ул. Примерная, 1")
        ], tight=True),
        actions=[ft.TextButton("Закрыть")]
    )

    medical_note_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Добавить запись в историю болезни"),
        content=new_note_field,
        actions=[
            ft.TextButton("Отмена"),
            ft.TextButton("Сохранить")
        ]
    )

    data_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Добавить показатели"),
        content=ft.Column(controls=data_fields),
        actions=[
            ft.TextButton("Отмена"),
            ft.TextButton("Сохранить")
        ]
    )

    # Добавляем диалоги в overlay страницы
    page.overlay.extend([contact_dialog, medical_note_dialog, data_dialog])

    # Функции обработчиков
    def close_dialog(e):
        page.dialog.open = False
        page.update()

    def open_contact_dialog(e):
        contact_dialog.actions[0].on_click = close_dialog
        page.dialog = contact_dialog
        contact_dialog.open = True
        page.update()

    def open_medical_note_dialog(e):
        new_note_field.value = ""
        medical_note_dialog.actions[0].on_click = close_dialog
        medical_note_dialog.actions[1].on_click = save_medical_note
        page.dialog = medical_note_dialog
        medical_note_dialog.open = True
        page.update()

    def open_data_dialog(e):
        new_note_field.value = ""
        data_dialog.actions[0].on_click = close_dialog
        data_dialog.actions[1].on_click = save_data
        page.dialog = data_dialog
        data_dialog.open = True
        page.update()

    def save_medical_note(e):
        if new_note_field.value.strip():
            conn = sqlite3.connect("chronic_diseases.db")
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE patients 
                SET medical_history = COALESCE(medical_history || '\n', '') || ?
                WHERE id = ?
            ''', (f"{datetime.now().strftime('%Y-%m-%d')}: {new_note_field.value}", patient_id))
            conn.commit()
            conn.close()

            medical_note_dialog.open = False
            page.update()

            # Обновляем страницу для отображения изменений
            doctor_patient_page(page, patient_id)

        # Поля для ввода значений

    rate_field = ft.TextField(label="Частота пульса (уд/мин)", keyboard_type=ft.KeyboardType.NUMBER)
    systolic_field = ft.TextField(label="Систолическое давление", keyboard_type=ft.KeyboardType.NUMBER)
    diastolic_field = ft.TextField(label="Диастолическое давление", keyboard_type=ft.KeyboardType.NUMBER)
    sugar_field = ft.TextField(label="Уровень сахара (ммоль/л)", keyboard_type=ft.KeyboardType.NUMBER)

    def save_data(e):
        try:
            rate = int(data_fields[0].value)
            systolic = int(data_fields[1].value)
            diastolic = int(data_fields[2].value)
            sugar = float(data_fields[3].value)
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("Пожалуйста, введите корректные значения."), open=True)
            page.update()
            return

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn = sqlite3.connect("chronic_diseases.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO heart_rates (patient_id, rate, measurement_time) VALUES (?, ?, ?)",
                       (patient_id, rate, now))
        cursor.execute(
            "INSERT INTO blood_pressure (patient_id, systolic, diastolic, measurement_time) VALUES (?, ?, ?, ?)",
            (patient_id, systolic, diastolic, now))
        cursor.execute("INSERT INTO blood_sugar (patient_id, level, measurement_time) VALUES (?, ?, ?)",
                       (patient_id, sugar, now))
        conn.commit()
        conn.close()

        data_dialog.open = False
        page.update()

        # Обновляем страницу для отображения изменений
        doctor_patient_page(page, patient_id)

    def go_back(e):
        page.go("/doctor")

    # Левая колонка - информация о пациенте
    info_table = ft.DataTable(
        column_spacing=20,
        horizontal_margin=10,
        columns=[
            ft.DataColumn(ft.Text("Параметр", size=14, weight="bold")),
            ft.DataColumn(ft.Text("Значение", size=14)),
        ],
        rows=[
            ft.DataRow(cells=[
                ft.DataCell(ft.Text("ФИО:", size=14)),
                ft.DataCell(ft.Text(name, size=14)),
            ]),
            ft.DataRow(cells=[
                ft.DataCell(ft.Text("Возраст:", size=14)),
                ft.DataCell(ft.Text(f"{age} лет", size=14)),
            ]),
            ft.DataRow(cells=[
                ft.DataCell(ft.Text("Курение:", size=14)),
                ft.DataCell(ft.Text("Да" if smoking else "Нет", size=14)),
            ]),
            ft.DataRow(cells=[
                ft.DataCell(ft.Text("Алкоголь:", size=14)),
                ft.DataCell(ft.Text("Да" if alcohol else "Нет", size=14)),
            ]),
        ],
    )

    # Блок истории болезней с возможностью редактирования
    history_header = ft.Row(
        controls=[
            ft.Text("История болезней:", size=18, weight="bold"),
            ft.IconButton(
                icon=ft.icons.ADD,
                tooltip="Добавить запись",
                on_click=lambda e: open_medical_note_dialog(e)
            )
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
    )

    medical_history_display = ft.ListView(
        controls=[ft.Text(medical_history if medical_history else "Нет данных", size=16)],
        height=200,
        spacing=10,
        padding=10,
        auto_scroll=True
    )

    history_card = ft.Card(
        content=ft.Container(
            content=ft.Column(
                controls=[
                    history_header,
                    ft.Divider(),
                    medical_history_display
                ],
                spacing=10
            ),
            padding=15,
            border_radius=10
        ),
        elevation=5
    )

    # Правая колонка - графики
    def create_chart(data, title, y_label, x_label="Дни наблюдения"):
        data_range = max(data) - min(data) if data else 1
        y_step = max(1, round(data_range / 5))

        return ft.Container(
            content=ft.Column([
                ft.Text(title, size=16, weight="bold"),
                ft.Row([
                    ft.Container(
                        ft.Text(y_label, size=12, color=ft.colors.GREY, rotate=0),
                        width=40,
                        alignment=ft.alignment.center
                    ),
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

    # Создаем кнопки
    action_buttons = ft.Row(
        controls=[
            ft.ElevatedButton(
                text="Назад к списку",
                on_click=go_back,
                width=200,
                height=40
            ),
            ft.ElevatedButton(
                text="Связаться с пациентом",
                on_click=open_contact_dialog,
                width=200,
                height=40,
                icon=ft.icons.CONTACT_PHONE
            ),
            ft.ElevatedButton(
                text="Добавить данные",
                on_click=open_data_dialog,
                width=200,
                height=40,
                icon=ft.icons.ADD_CIRCLE_OUTLINE
            ),
            ft.ElevatedButton(
                text="Добавить запись",
                on_click=open_medical_note_dialog,
                width=200,
                height=40,
                icon=ft.icons.ADD_CIRCLE_OUTLINE
            )
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER
    )

    # Основной интерфейс с закрепленной сверху таблицей
    page.clean()
    page.add(
        ft.Column(
            controls=[
                # Шапка с названием
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Text(f"Карта пациента: {name}", size=24, weight="bold"),
                            ft.Text(f"ID: {patient_id}", color=ft.colors.GREY_600)
                        ],
                        spacing=10
                    ),
                    padding=ft.padding.only(bottom=15)
                ),

                # Фиксированная таблица (не прокручивается)


                # Прокручиваемая область (графики + история)
                ft.Column(
                    controls=[
                        ft.Card(
                            content=ft.Container(
                                content=info_table,
                                padding=20,
                            ),
                            elevation=2,
                            width=page.width - 40  # Ширина с отступами
                        ),
                        # Графики
                        ft.Container(
                            content=scrollable_charts,
                            padding=10,
                        ),

                        # История болезней
                        history_card,
                    ],
                    expand=True,
                    scroll=ft.ScrollMode.AUTO
                ),

                # Фиксированные кнопки внизу
                ft.Container(
                    content=action_buttons,
                    padding=15,
                    bgcolor=ft.colors.GREY_50,
                    border_radius=ft.border_radius.only(top_left=10, top_right=10),
                    border=ft.border.all(1, ft.colors.GREY_200)
                )
            ],
            expand=True,
            spacing=15
        )
    )

    # Функция обновления истории болезней
    def update_history_display():
        # Получаем данные из БД
        conn = sqlite3.connect("chronic_diseases.db")
        cursor = conn.cursor()
        cursor.execute('SELECT medical_history FROM patients WHERE id = ?', (patient_id,))
        result = cursor.fetchone()
        new_history = result[0] if result else None
        conn.close()

        # Обновляем отображение с помощью list comprehension
        medical_history_display.controls = (
            [ft.Text(line, size=16) for line in new_history.split('\n') if line.strip()]
            if new_history
            else [ft.Text("Нет данных", size=16, color=ft.colors.GREY_600)]
        )
        page.update()

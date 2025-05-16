import flet as ft
import sqlite3
from datetime import datetime
import random


def calculate_age(date_of_birth):
    today = datetime.today()
    birth_date = datetime.strptime(date_of_birth, "%Y-%m-%d")
    age = today.year - birth_date.year
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        age -= 1
    return age


def generate_random_data():
    return {
        "heart_rate": [random.randint(60, 100) for _ in range(30)],
        "blood_pressure": [(random.randint(110, 130), random.randint(70, 90)) for _ in range(30)],
        "blood_sugar": [random.randint(70, 120) for _ in range(30)],
    }


def patient_page(page: ft.Page):
    # Получаем логин авторизованного пациента из сессии
    patient_login = page.session.get("user_login")
    if not patient_login:
        page.go("/")
        return

    # Получаем данные пациента из БД
    conn = sqlite3.connect("chronic_diseases.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT p.id, p.name, p.date_of_birth, p.smoking, p.alcohol, p.medical_history, p.contact_info
        FROM patients p
        JOIN patient_auth pa ON p.id = pa.patient_id
        WHERE pa.login = ?
    ''', (patient_login,))
    patient_data = cursor.fetchone()
    conn.close()

    if not patient_data:
        page.add(ft.Text("Данные пациента не найдены", size=24, weight="bold"))
        return

    patient_id, name, date_of_birth, smoking, alcohol, medical_history, contact_info = patient_data
    age = calculate_age(date_of_birth)
    data = generate_random_data()

    # Генерация случайных данных для графиков
    data = generate_random_data()

    # Создаем элементы диалогов заранее
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

    # Добавляем диалоги в overlay страницы
    page.overlay.extend([contact_dialog, medical_note_dialog])

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

    def go_back(e):
        page.go("/")

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
                tooltip="Добавить запись как пациент",
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
                text="Назад",
                on_click=go_back,
                width=200,
                height=40
            ),
            ft.ElevatedButton(
                text="Добавить запись как пациент",
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

        # Модифицируем функцию сохранения записи

    def save_medical_note(e):
        if new_note_field.value.strip():
            conn = sqlite3.connect("chronic_diseases.db")
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE patients 
                SET medical_history = COALESCE(medical_history || '\n', '') || ?
                WHERE id = ?
            ''', (f"{datetime.now().strftime('%Y-%m-%d')} [запись пациента]: {new_note_field.value}", patient_id))
            conn.commit()
            conn.close()

            medical_note_dialog.open = False
            page.update()

            # Обновляем страницу для отображения изменений
            update_history_display()
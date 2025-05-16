# create_patient_data.py
import sqlite3
import random
from datetime import datetime, timedelta


def init_patient_tables():
    conn = sqlite3.connect("chronic_diseases.db")
    cursor = conn.cursor()

    # Таблица для показателей сердца
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS heart_rates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            rate INTEGER NOT NULL,
            measurement_time TEXT NOT NULL,
            FOREIGN KEY (patient_id) REFERENCES patients (id)
        )
    ''')

    # Таблица для артериального давления
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blood_pressure (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            systolic INTEGER NOT NULL,
            diastolic INTEGER NOT NULL,
            measurement_time TEXT NOT NULL,
            FOREIGN KEY (patient_id) REFERENCES patients (id)
        )
    ''')

    # Таблица для уровня сахара
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blood_sugar (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            level REAL NOT NULL,
            measurement_time TEXT NOT NULL,
            FOREIGN KEY (patient_id) REFERENCES patients (id)
        )
    ''')

    conn.commit()
    conn.close()


def generate_test_data(patient_id, days=30):
    conn = sqlite3.connect("chronic_diseases.db")
    cursor = conn.cursor()

    base_date = datetime.now() - timedelta(days=days)

    # Генерация данных ЧСС
    for day in range(days):
        current_date = base_date + timedelta(days=day)
        for hour in [8, 12, 18]:  # 3 измерения в день
            rate = random.randint(60, 100)
            if day % 7 == 0:  # Раз в неделю "аномалия"
                rate += random.choice([-15, 15])
            cursor.execute(
                "INSERT INTO heart_rates (patient_id, rate, measurement_time) VALUES (?, ?, ?)",
                (patient_id, rate, current_date.replace(hour=hour).strftime("%Y-%m-%d %H:%M:%S"))
            )

    # Генерация данных давления
    for day in range(days):
        current_date = base_date + timedelta(days=day)
        systolic = random.randint(110, 130)
        diastolic = random.randint(70, 90)
        if day % 5 == 0:  # Раз в 5 дней "аномалия"
            systolic += random.choice([-10, 10])
            diastolic += random.choice([-5, 5])
        cursor.execute(
            "INSERT INTO blood_pressure (patient_id, systolic, diastolic, measurement_time) VALUES (?, ?, ?, ?)",
            (patient_id, systolic, diastolic, current_date.strftime("%Y-%m-%d %H:%M:%S"))
        )

    # Генерация данных сахара
    for day in range(days):
        current_date = base_date + timedelta(days=day)
        level = random.uniform(3.9, 6.1)  # Нормальный уровень
        if day % 3 == 0:  # Раз в 3 дня "аномалия"
            level += random.choice([-1.5, 1.5])
        cursor.execute(
            "INSERT INTO blood_sugar (patient_id, level, measurement_time) VALUES (?, ?, ?)",
            (patient_id, round(level, 1), current_date.strftime("%Y-%m-%d %H:%M:%S"))
        )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_patient_tables()
    # Предполагаем, что тестовый пациент имеет id=1
    generate_test_data(patient_id=1)
    print("Тестовые данные пациентов успешно созданы!")
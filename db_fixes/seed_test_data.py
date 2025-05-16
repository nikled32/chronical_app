import sqlite3
import random
from datetime import datetime, timedelta


def seed_test_data():
    conn = sqlite3.connect("../chronic_diseases.db")
    cursor = conn.cursor()

    # Очищаем существующие данные (опционально)
    cursor.execute("DELETE FROM patients")
    cursor.execute("DELETE FROM heart_rate")
    cursor.execute("DELETE FROM blood_pressure")
    cursor.execute("DELETE FROM blood_sugar")

    # Список тестовых пациентов
    test_patients = [
        ("Иванов Иван Иванович", "М", "1980-05-15", "ivanov@example.com"),
        ("Петрова Мария Сергеевна", "Ж", "1975-11-22", "petrova@example.com"),
        ("Сидоров Алексей Владимирович", "М", "1990-03-10", "sidorov@example.com"),
        ("Кузнецова Елена Дмитриевна", "Ж", "1988-07-30", "kuznetsova@example.com"),
        ("Васильев Дмитрий Олегович", "М", "1972-01-18", "vasilev@example.com"),
        ("Николаева Анна Петровна", "Ж", "1995-09-05", "nikolaeva@example.com"),
        ("Федоров Сергей Викторович", "М", "1983-12-12", "fedorov@example.com"),
        ("Михайлова Ольга Игоревна", "Ж", "1978-04-25", "mikhailova@example.com"),
        ("Павлов Артем Александрович", "М", "1992-08-08", "pavlov@example.com"),
        ("Семенова Виктория Андреевна", "Ж", "1985-06-20", "semenova@example.com")
    ]

    # Добавляем пациентов
    for patient in test_patients:
        cursor.execute(
            "INSERT INTO patients (name, gender, date_of_birth, contact_info) VALUES (?, ?, ?, ?)",
            patient
        )
        patient_id = cursor.lastrowid

        # Генерируем медицинские данные за последние 30 дней
        for days_ago in range(30, 0, -1):
            record_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")

            # ЧСС (60-100 уд/мин)
            cursor.execute(
                "INSERT INTO heart_rate (patient_id, rate, record_date) VALUES (?, ?, ?)",
                (patient_id, random.randint(60, 100), record_date)
            )

            # Артериальное давление (110-130/70-90)
            cursor.execute(
                "INSERT INTO blood_pressure (patient_id, systolic, diastolic, record_date) VALUES (?, ?, ?, ?)",
                (patient_id, random.randint(110, 130), random.randint(70, 90), record_date)
            )

            # Уровень сахара (70-120 мг/дл)
            cursor.execute(
                "INSERT INTO blood_sugar (patient_id, sugar_level, record_date) VALUES (?, ?, ?)",
                (patient_id, random.randint(70, 120), record_date)
            )

    print("Тестовые данные для 10 пациентов успешно добавлены!")
    conn.commit()
    conn.close()


if __name__ == "__main__":
    seed_test_data()

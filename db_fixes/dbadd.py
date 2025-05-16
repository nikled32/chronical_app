import sqlite3
from datetime import datetime, timedelta
import random


# Функция для генерации случайной даты рождения
def generate_random_date_of_birth():
    start_date = datetime(1950, 1, 1)
    end_date = datetime(2005, 12, 31)
    random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    return random_date.strftime("%Y-%m-%d")  # Формат ГГГГ-ММ-ДД


# Функция для добавления пациентов
def add_patients():
    conn = sqlite3.connect("../chronic_diseases.db")
    cursor = conn.cursor()

    # Список тестовых данных
    patients = [
        ("Иван Иванов", "Мужской", "ivan@example.com", generate_random_date_of_birth(), 1, 0, "Гипертония, диабет"),
        ("Мария Петрова", "Женский", "maria@example.com", generate_random_date_of_birth(), 0, 1, "Астма"),
        ("Алексей Сидоров", "Мужской", "alex@example.com", generate_random_date_of_birth(), 0, 1, "Высокое КД"),
        ("Ольга Кузнецова", "Женский", "olga@example.com", generate_random_date_of_birth(), 1, 1, "Диабет"),
        ("Дмитрий Смирнов", "Мужской", "dmitry@example.com", generate_random_date_of_birth(), 0, 0, "Нет заболеваний"),
        ("Елена Васильева", "Женский", "elena@example.com", generate_random_date_of_birth(), 1, 0, "Заболевания ССС"),
        ("Сергей Павлов", "Мужской", "sergey@example.com", generate_random_date_of_birth(), 0, 1, "Артрит"),
        ("Анна Козлова", "Женский", "anna@example.com", generate_random_date_of_birth(), 1, 1, "Аллергии"),
        ("Николай Новиков", "Мужской", "nikolay@example.com", generate_random_date_of_birth(), 0, 0, "Мигрени"),
        ("Татьяна Морозова", "Женский", "tatyana@example.com", generate_random_date_of_birth(), 0, 1, "Операция"),
    ]

    # Вставка данных в таблицу
    cursor.executemany('''
        INSERT INTO patients (name, gender, contact_info, date_of_birth, smoking, alcohol, medical_history)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', patients)

    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()

    print("Добавлено 10 записей пациентов.")


# Запуск функции для добавления пациентов
if __name__ == "__main__":
    add_patients()
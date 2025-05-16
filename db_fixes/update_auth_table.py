import sqlite3
import hashlib


def update_auth_tables():
    conn = sqlite3.connect("../chronic_diseases.db")
    cursor = conn.cursor()

    # Создаем таблицу для авторизации пациентов, если не существует
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patient_auth (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL UNIQUE,
            login TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            FOREIGN KEY (patient_id) REFERENCES patients (id)
        )
    ''')

    # Создаем таблицу для авторизации врачей, если не существует
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS auth_doctor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doctor_id INTEGER NOT NULL UNIQUE,
            login TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            FOREIGN KEY (doctor_id) REFERENCES doctors (id)
        )
    ''')

    # Добавляем тестовых врачей, если их нет
    cursor.execute("SELECT COUNT(*) FROM doctors")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO doctors (name, specialization, contact_info) VALUES (?, ?, ?)",
            ("Смирнов Александр Викторович", "Кардиолог", "cardio@hospital.ru")
        )
        doctor_id = cursor.lastrowid

        # Хеш пароля "doctor123"
        password_hash = hashlib.sha256("doctor123".encode()).hexdigest()
        cursor.execute(
            "INSERT INTO auth_doctor (doctor_id, login, password_hash) VALUES (?, ?, ?)",
            (doctor_id, "cardio@hospital.ru", password_hash)
        )

    # Обновляем записи авторизации для пациентов
    cursor.execute("SELECT id, contact_info FROM patients")
    patients = cursor.fetchall()

    # Хеш пароля "patient123" (для всех пациентов)
    password_hash = hashlib.sha256("patient123".encode()).hexdigest()

    for patient_id, contact_info in patients:
        try:
            cursor.execute(
                "INSERT INTO patient_auth (patient_id, login, password_hash) VALUES (?, ?, ?)",
                (patient_id, contact_info, password_hash)
            )
        except sqlite3.IntegrityError:
            # Если запись уже существует, пропускаем
            continue

    print("Таблицы авторизации успешно обновлены!")
    conn.commit()
    conn.close()


if __name__ == "__main__":
    update_auth_tables()
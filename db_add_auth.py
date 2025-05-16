# db_add_auth.py
import sqlite3
import hashlib
import secrets


def init_db():
    """Инициализация всех таблиц базы данных"""
    conn = sqlite3.connect("chronic_diseases.db")
    cursor = conn.cursor()

    # Основные таблицы (если еще не созданы)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialization TEXT NOT NULL,
            contact_info TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            gender TEXT NOT NULL,
            date_of_birth TEXT,
            contact_info TEXT
        )
    ''')

    # Таблицы для авторизации
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS doctor_auth (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doctor_id INTEGER NOT NULL,
            login TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            FOREIGN KEY (doctor_id) REFERENCES doctors (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patient_auth (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            login TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            FOREIGN KEY (patient_id) REFERENCES patients (id)
        )
    ''')

    conn.commit()
    conn.close()


def hash_password(password: str, salt: str = None) -> tuple:
    """Генерация хэша пароля с солью"""
    if not salt:
        salt = secrets.token_hex(16)
    pw_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    ).hex()
    return pw_hash, salt


def add_test_users():
    """Добавление тестовых пользователей в базу данных"""
    conn = sqlite3.connect("chronic_diseases.db")
    cursor = conn.cursor()

    try:
        # Добавляем тестового врача
        cursor.execute('''
            INSERT OR IGNORE INTO doctors (id, name, specialization, contact_info)
            VALUES (1, 'Доктор Иванов', 'Кардиолог', 'ivanov@clinic.ru')
        ''')

        doctor_hash, doctor_salt = hash_password("doctor123")
        cursor.execute('''
            INSERT OR REPLACE INTO doctor_auth 
            (doctor_id, login, password_hash, salt)
            VALUES (1, 'doctor1', ?, ?)
        ''', (doctor_hash, doctor_salt))

        # Добавляем тестового пациента
        cursor.execute('''
            INSERT OR IGNORE INTO patients (id, name, gender, date_of_birth, contact_info)
            VALUES (1, 'Пациент Петров', 'М', '1980-05-15', 'petrov@mail.ru')
        ''')

        patient_hash, patient_salt = hash_password("patient123")
        cursor.execute('''
            INSERT OR REPLACE INTO patient_auth 
            (patient_id, login, password_hash, salt)
            VALUES (1, 'patient1', ?, ?)
        ''', (patient_hash, patient_salt))

        conn.commit()
        print("Тестовые пользователи успешно добавлены!")

    except sqlite3.Error as e:
        print(f"Ошибка при добавлении тестовых пользователей: {e}")
    finally:
        conn.close()


def check_credentials(login: str, password: str, role: str) -> bool:
    """Проверка учетных данных в базе данных"""
    conn = sqlite3.connect("chronic_diseases.db")
    cursor = conn.cursor()

    try:
        table = 'doctor_auth' if role == 'doctor' else 'patient_auth'
        cursor.execute(f'''
            SELECT password_hash, salt FROM {table} WHERE login = ?
        ''', (login,))

        result = cursor.fetchone()
        if not result:
            return False

        stored_hash, salt = result
        input_hash, _ = hash_password(password, salt)
        return stored_hash == input_hash

    except sqlite3.Error as e:
        print(f"Ошибка проверки учетных данных: {e}")
        return False
    finally:
        conn.close()


if __name__ == "__main__":
    init_db()
import sqlite3


# Создание и подключение к базе данных
def create_database():
    conn = sqlite3.connect("chronic_diseases.db")
    cursor = conn.cursor()

    # Таблица для врачей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialization TEXT NOT NULL,
            contact_info TEXT
        )
    ''')

    # Таблица для пациентов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            gender TEXT NOT NULL,
            date_of_birth TEXT,
            contact_info TEXT
        )
    ''')

    # Таблица для диагнозов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS diagnoses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            diagnosis TEXT NOT NULL,
            date_diagnosed TEXT NOT NULL,
            FOREIGN KEY (patient_id) REFERENCES patients (id),
            FOREIGN KEY (doctor_id) REFERENCES doctors (id)
        )
    ''')

    # Таблица для записей о состоянии здоровья
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS health_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            record_date TEXT NOT NULL,
            symptoms TEXT,
            treatment TEXT,
            notes TEXT,
            FOREIGN KEY (patient_id) REFERENCES patients (id)
        )
    ''')

    conn.commit()
    conn.close()


# Инициализация базы данных
if __name__ == "__main__":
    create_database()
    print("База данных успешно создана!")
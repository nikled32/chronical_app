import hashlib
import sqlite3


def add_doctor(name, specialization, email, password):
    conn = sqlite3.connect("../chronic_diseases.db")
    cursor = conn.cursor()

    try:
        # Добавляем врача
        cursor.execute(
            "INSERT INTO doctors (name, specialization, contact_info) VALUES (?, ?, ?)",
            (name, specialization, email)
        )
        doctor_id = cursor.lastrowid

        # Добавляем запись для авторизации
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute(
            "INSERT INTO auth_doctor (doctor_id, password_hash) VALUES (?, ?)",
            (doctor_id, password_hash)
        )

        conn.commit()
        return doctor_id
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()
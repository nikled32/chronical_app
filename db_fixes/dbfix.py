import sqlite3

# Подключение к базе данных
conn = sqlite3.connect("../chronic_diseases.db")
cursor = conn.cursor()

# Добавление нового столбца "last_accessed" в таблицу "patients"
cursor.execute("ALTER TABLE patients ADD COLUMN smoking")
cursor.execute("ALTER TABLE patients ADD COLUMN alcohol")
cursor.execute("ALTER TABLE patients ADD COLUMN medical_history")
# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()
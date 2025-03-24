import sqlite3


def delete_all_records(database_name, table_name):
    try:
        # Подключаемся к базе данных
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()

        # Запрос на удаление всех записей из таблицы
        cursor.execute(f"DELETE FROM {table_name}")

        # Сохраняем изменения
        conn.commit()
        print(f"Все записи из таблицы '{table_name}' были успешно удалены.")

    except sqlite3.Error as e:
        print(f"Ошибка при работе с SQLite: {e}")
    finally:
        # Закрываем соединение
        if conn:
            conn.close()


# Укажите имя вашей базы данных и таблицы
database_name = 'chronic_diseases.db'
table_name = 'patients'

# Вызываем функцию удаления всех записей
delete_all_records(database_name, table_name)

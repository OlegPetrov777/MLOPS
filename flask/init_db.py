import sqlite3
import os

DB_NAME = 'logs.db'

def create_database():
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                age_group TEXT,
                platform TEXT,
                special_device TEXT,
                price REAL,
                release_year INTEGER,
                game_length REAL,
                min_players INTEGER,
                prediction REAL
            )
        ''')
        conn.commit()
        conn.close()
        print("База данных и таблица успешно созданы.")
    else:
        print("База данных уже существует.")

if __name__ == "__main__":
    create_database()

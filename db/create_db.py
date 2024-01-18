import sqlite3
from models import create_tables

def create_database():
    conn = sqlite3.connect('dbVideos.db')
    cursor = conn.cursor()

    create_tables(cursor)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    print("Base de datos creada con éxito.")

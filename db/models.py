import sqlite3

def create_tables(cursor):
    try:
      # cursor.execute('''CREATE TABLE IF NOT EXISTS User (
      #                         id INTEGER PRIMARY KEY AUTOINCREMENT,
      #                         username TEXT NOT NULL UNIQUE,
      #                         password TEXT NOT NULL,
      #                         email TEXT NOT NULL UNIQUE
      #                     )''')

      # cursor.execute('''CREATE TABLE IF NOT EXISTS Videos (
      #                         video_id INTEGER PRIMARY KEY AUTOINCREMENT,
      #                         id_user INTEGER,
      #                         titulo TEXT NOT NULL,
      #                         fecha_subida DATE NOT NULL,
      #                         fps REAL NOT NULL,
      #                         FOREIGN KEY (id_user) REFERENCES User(id)
      #                     )''')
      cursor.execute('''CREATE TABLE IF NOT EXISTS Videos (
                              video_id INTEGER PRIMARY KEY AUTOINCREMENT,
                              fecha_subida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                              fps REAL NOT NULL
                          )''')
      
      cursor.execute('''CREATE TABLE IF NOT EXISTS framesData (
                              frame_id INTEGER PRIMARY KEY AUTOINCREMENT,
                              video_id INTEGER,
                              tipo TEXT NOT NULL CHECK(tipo IN ('original', 'copia', 'mascara')),
                              ruta_archivo TEXT NOT NULL,
                              indice INTEGER NOT NULL,
                              FOREIGN KEY (video_id) REFERENCES Videos(video_id)
                          )''')
    except sqlite3.Error as e:
            print(f"An error occurred: {e.args[0]}")

   

    
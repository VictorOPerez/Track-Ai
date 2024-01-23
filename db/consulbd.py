import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('dbVideos.db')
cursor = conn.cursor()

# Obtener una lista de todas las tablas en la base de datos
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tablas = cursor.fetchall()

# Recorrer todas las tablas y mostrar sus columnas
for tabla in tablas:
    print(f"Tabla: {tabla[0]}")
    cursor.execute(f"PRAGMA table_info({tabla[0]});")
    columnas = cursor.fetchall()
    for col in columnas:
        print(col)

# Cerrar el cursor y la conexión
cursor.close()
conn.close()

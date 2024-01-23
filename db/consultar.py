import sqlite3

# Establecer conexión con la base de datos
conn = sqlite3.connect('dbVideos.db')

# Crear un cursor
cursor = conn.cursor()

# Ejecutar una sentencia SQL de consulta
consulta_sql = "SELECT * FROM framesData"  # Reemplaza 'tu_tabla' con el nombre de tu tabla
cursor.execute(consulta_sql)

# Recuperar los resultados
resultados = cursor.fetchall()
print(resultados, "resultados")
for fila in resultados:
    print(fila)

# Cerrar el cursor y la conexión
cursor.close()
conn.close()

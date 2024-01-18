import sqlite3

def registrar_frame_en_bd(conn, video_id, indice, ruta_archivo, tipo):
    try:
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO framesData (video_id, tipo, ruta_archivo, indice)
                          VALUES (?, ?, ?, ?)''',
                          (video_id, tipo, ruta_archivo, indice))
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e.args[0]}")

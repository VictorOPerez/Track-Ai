import sqlite3

def obtener_ruta_frame(video_id, frame_indice):
    conn = sqlite3.connect('mydatabase.db')
    try:
        cursor = conn.cursor()
        cursor.execute('''SELECT ruta_archivo FROM framesData
                          WHERE video_id = ? AND indice = ?''', (video_id, frame_indice))
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        conn.close()

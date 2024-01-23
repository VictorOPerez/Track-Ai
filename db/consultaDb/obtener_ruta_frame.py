import sqlite3

def obtener_ruta_frame(video_id, frame_indice):
    print("aqui dentro de obtener_ruta_frame")

    conn = sqlite3.connect('db/dbVideos.db')

    print("aqui despues de la coneccion a la base de datos")
    try:
        cursor = conn.cursor()
        cursor.execute('''SELECT ruta_archivo FROM framesData
                          WHERE video_id = ? AND indice = ?''', (video_id, frame_indice))
        resultado = cursor.fetchall()
        print("aqui despues de optener la ruta resultado[0]",resultado)
        return resultado if resultado else None
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        conn.close()

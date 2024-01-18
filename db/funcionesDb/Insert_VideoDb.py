import sqlite3
from crear_carpeta_para_video import crear_carpeta_para_video

def Insert_VideoDb(conn, fps):
    # video_data es un diccionario con el título, descripción, fecha de subida, etc.
      try:
          cursor = conn.cursor()
          
          # Insertar la información del video en la base de datos
          cursor.execute('''INSERT INTO Videos ( fecha_subida, fps)
                  VALUES (CURRENT_TIMESTAMP, ?)''',
                  (  fps))
          
          video_id = cursor.lastrowid          
          conn.commit()
          crear_carpeta_para_video(video_id)
             
          return video_id
      except sqlite3.Error as e:
          print(f"An error occurred: {e.args[0]}")
          return None

      # conn = sqlite3.connect('mydatabase.db')  # Conectar a la base de datos
      # user_id = 1  # El ID del usuario que sube el video
      # video_id = upload_video(conn, user_id, video_data, video_file_path)
      # if video_id:
      #     print(f"Video uploaded successfully with ID: {video_id}")
      # else:
      #     print("Failed to upload video.")

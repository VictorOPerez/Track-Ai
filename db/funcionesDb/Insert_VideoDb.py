import sqlite3
from db.funcionesDb.crear_carpeta_para_video import crear_carpeta_para_video

def Insert_VideoDb(cursor, fps):

      print("insert video despues")

      try:
                  
          # Insertar la información del video en la base de datos
          cursor.execute('''INSERT INTO Videos ( fecha_subida, fps)
                  VALUES (CURRENT_TIMESTAMP, ?)''',
                  (  fps, ))
          
          video_id = cursor.lastrowid          
          crear_carpeta_para_video(video_id)
          print("insert video id ", video_id)

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

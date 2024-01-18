import time
import cv2
import psutil
import os
import numpy as np
import sqlite3
from db.funcionesDb.Insert_VideoDb import Insert_VideoDb
from db.funcionesDb.guardar_frame import guardar_frame
from db.funcionesDb.registrar_frame_en_bd import registrar_frame_en_bd

def get_frames_from_video(video_path):
    from app import model
    try:
        conn = sqlite3.connect('dbVideos.db')
        # frames = []  # Inicializa una lista para almacenar los fotogramas del video.
        # user_name = time.time()  # Genera un identificador único para el usuario basado en el tiempo actual.
        
        # Define un log de operaciones inicial.
        operation_log = [("",""),("Upload video already. Try click the image for adding targets to track and inpaint.","Normal")]

        # try:
        cap = cv2.VideoCapture(video_path)  # Intenta abrir el video para la lectura de fotogramas.
        fps = cap.get(cv2.CAP_PROP_FPS)  # Obtiene el número de fotogramas por segundo del video.
        video_id = Insert_VideoDb(conn,fps)
        # Bucle para leer los fotogramas del video.
        indice = 0
        while cap.isOpened():
            ret, frame = cap.read()  # Lee el siguiente fotograma del video.
            if ret == True:
                # Verifica el uso actual de memoria del sistema.
                current_memory_usage = psutil.virtual_memory().percent
                ruta_frame= guardar_frame(video_id, frame ,indice,'original')

                frame_copia = frame.copy()
                ruta_frame_copia = guardar_frame(video_id, frame_copia, indice, 'copia')

                mask = np.zeros((frame.shape[0], frame.shape[1]), np.uint8)
                ruta_mask = guardar_frame(video_id, mask, indice, 'mask')

                registrar_frame_en_bd(conn,video_id,indice, ruta_frame,"original" )
                registrar_frame_en_bd(conn,video_id,indice, ruta_frame_copia,"copia" )
                registrar_frame_en_bd(conn,video_id,indice, ruta_mask,"mask" )
                #

                # Si el uso de memoria supera el 90%, se registra un mensaje de error y se detiene la extracción.
                indice += 1
                if current_memory_usage > 90:
                    operation_log = [("Memory usage is too high (>90%). Stop the video extraction. Please reduce the video resolution or frame rate.", "Error")]
                    print("Memory usage is too high (>90%). Please reduce the video resolution or frame rate.")
                    # break
                    
            else:
                break
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Cierra la conexión aquí, en el bloque finally
        if conn:
            conn.close()
    return fps
    # except (OSError, TypeError, ValueError, KeyError, SyntaxError) as e:
    #     # Maneja excepciones durante la lectura del video y registra errores.
    #     print("read_frame_source:{} error. {}\n".format(video_path, str(e)))

    # Obtiene el tamaño de los fotogramas (ancho y alto).
    # image_size = (frames[0].shape[0],frames[0].shape[1])

    # Inicializa y actualiza el estado del video con información relevante.
    # video_state = {
    #     "user": user_name,# Almacena un identificador único para el usuario.       
    #     "vname": os.path.split(video_path)[-1], # Guarda el nombre del archivo de video.
    #     "frame": frames,# Contiene una lista de los fotogramas originales del video.
    #     "fcopy": frames.copy(),# Almacena una copia de los fotogramas originales.
    #     "masks": [np.zeros((frames[0].shape[0],frames[0].shape[1]), np.uint8)]*len(frames), # Crea una lista de máscaras,      
    #     "logits": [None]*len(frames),  # Inicializa una lista de 'logits',
    #     "fps":fps # Valor faltante aquí
    # }
    # Devuelve el estado del video, la información del video,
    # return video_state

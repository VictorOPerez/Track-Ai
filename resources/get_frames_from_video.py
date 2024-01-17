import time
import cv2
import psutil
import os
import numpy as np

def get_frames_from_video(video_input):
    from app import model

    video_path = video_input  # Almacena la ruta del video proporcionada en la variable video_path.
    frames = []  # Inicializa una lista para almacenar los fotogramas del video.
    user_name = time.time()  # Genera un identificador único para el usuario basado en el tiempo actual.

    # Define un log de operaciones inicial.
    operation_log = [("",""),("Upload video already. Try click the image for adding targets to track and inpaint.","Normal")]

    try:
        cap = cv2.VideoCapture(video_path)  # Intenta abrir el video para la lectura de fotogramas.
        fps = cap.get(cv2.CAP_PROP_FPS)  # Obtiene el número de fotogramas por segundo del video.

        # Bucle para leer los fotogramas del video.
        while cap.isOpened():
            ret, frame = cap.read()  # Lee el siguiente fotograma del video.
            if ret == True:
                # Verifica el uso actual de memoria del sistema.
                current_memory_usage = psutil.virtual_memory().percent

                # Añade el fotograma a la lista de frames después de convertirlo de BGR a RGB.
                frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

                # Si el uso de memoria supera el 90%, se registra un mensaje de error y se detiene la extracción.
                if current_memory_usage > 90:
                    operation_log = [("Memory usage is too high (>90%). Stop the video extraction. Please reduce the video resolution or frame rate.", "Error")]
                    print("Memory usage is too high (>90%). Please reduce the video resolution or frame rate.")
                    # break
            else:
                break
    except (OSError, TypeError, ValueError, KeyError, SyntaxError) as e:
        # Maneja excepciones durante la lectura del video y registra errores.
        print("read_frame_source:{} error. {}\n".format(video_path, str(e)))

    # Obtiene el tamaño de los fotogramas (ancho y alto).
    image_size = (frames[0].shape[0],frames[0].shape[1])

    # Inicializa y actualiza el estado del video con información relevante.
    video_state = {
        "user": user_name,# Almacena un identificador único para el usuario.       
        "vname": os.path.split(video_path)[-1], # Guarda el nombre del archivo de video.
        "frame": frames,# Contiene una lista de los fotogramas originales del video.
        "fcopy": frames.copy(),# Almacena una copia de los fotogramas originales.
        "masks": [np.zeros((frames[0].shape[0],frames[0].shape[1]), np.uint8)]*len(frames), # Crea una lista de máscaras,      
        "logits": [None]*len(frames),  # Inicializa una lista de 'logits',
        "fps":fps # Valor faltante aquí
    }
    # Devuelve el estado del video, la información del video,
    return video_state

import time
import cv2
import psutil
import os
import numpy as np
from app import model

def get_frames_from_video(video_input):
    """
    Args:
        video_path:str
        timestamp:float64
    Return 
        [[0:nearest_frame], [nearest_frame:], nearest_frame]
    """

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
        # Almacena un identificador único para el usuario, probablemente basado en el tiempo actual.
        "user_name": user_name,

        # Guarda el nombre del archivo de video. Utiliza os.path.split para separar la ruta del archivo y [-1] para tomar solo el nombre del archivo.
        "video_name": os.path.split(video_path)[-1],

        # Contiene una lista de los fotogramas originales del video. Estos son los fotogramas sin modificar.
        "F_To_Image": frames,

        # Almacena una copia de los fotogramas originales. Esto sugiere que estos fotogramas podrían ser modificados o 'pintados' en procesos posteriores.
        "F_Orig": frames.copy(),

        # Crea una lista de máscaras, inicialmente establecidas en cero (negro) para cada fotograma del video. 
        # Estas máscaras son arrays de NumPy del mismo tamaño que los fotogramas y se utilizan para operaciones de procesamiento de imágenes, como seguimiento o edición de imágenes.
        "masks": [np.zeros((frames[0].shape[0],frames[0].shape[1]), np.uint8)]*len(frames),

        # Inicializa una lista de 'logits', probablemente destinada a almacenar resultados de modelos de aprendizaje automático o procesamiento de imágenes, para cada fotograma.
        "logits": [None]*len(frames),

        # Establece un contador o índice para el fotograma seleccionado actualmente, iniciando en 0.
        "indice_F_Act": 0,

        # Almacena la tasa de fotogramas por segundo (fps) del video.
        "fps":fps # Valor faltante aquí
    }


    # Formatea la información del video para su presentación.
    video_info = "Video Name: {}, FPS: {}, Total Frames: {}, Image Size:{}".format(video_state["video_name"], video_state["fps"], len(frames), image_size)
    print(f"fotogramos{video_state["fps"]},path{video_path}")
    # Restablece y establece la imagen en el controlador del modelo.
    model.samcontroler.sam_controler.reset_image()
    model.samcontroler.sam_controler.set_image(video_state["F_To_Image"][0])

    # Devuelve el estado del video, la información del video,
    return video_state

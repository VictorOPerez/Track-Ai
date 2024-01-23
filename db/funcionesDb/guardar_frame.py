import cv2
import os

def guardar_frame(video_id, frame, indice,tipo, formato='png'):
    nombre_carpeta = f"video_{video_id}"
    ruta_carpeta = os.path.join("db-Videos", nombre_carpeta)

    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)
        print()

    nombre_archivo = f"frame_{indice}_{tipo}.{formato}"
    ruta_archivo = os.path.join(ruta_carpeta, nombre_archivo)

    cv2.imwrite(ruta_archivo, frame)

    return ruta_archivo

# # Ejemplo de uso
# video_id = 123
# frames = [...]  # Suponiendo que tienes una lista de frames aquí
# for indice, frame in enumerate(frames):
#     ruta_archivo = guardar_frame(video_id, frame, indice)
#     print(f"Frame guardado en: {ruta_archivo}")

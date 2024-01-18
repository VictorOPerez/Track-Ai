import os

def crear_carpeta_para_video(video_id):
    # Construye el nombre de la carpeta basado en el video_id
    directorio_base="db-Videos"
    nombre_carpeta = f"video_{video_id}"
    ruta_carpeta = os.path.join(directorio_base, nombre_carpeta)

    # Comprueba si la carpeta ya existe, si no, créala
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)




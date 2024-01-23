import cv2

def guardar_imagen_modificada(ruta_archivo, imagen_modificada):
    try:
        print("antes de quitarle el RGB")
        image_to_save = cv2.cvtColor(imagen_modificada, cv2.COLOR_RGB2BGR)
        print("antes de guardar en la ruata")
        cv2.imwrite(ruta_archivo, image_to_save)
        print(f"Imagen guardada con éxito en: {ruta_archivo}")
    except Exception as e:
        print(f"Error al guardar la imagen: {e}")

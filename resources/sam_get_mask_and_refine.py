
from resources.get_prompt import get_prompt
from db.consultaDb.obtener_ruta_frame import obtener_ruta_frame
from db.funcionesDb.guardar_imagen_modificada import guardar_imagen_modificada
import numpy as np
import cv2

def sam_get_mask_and_refine(videoId, point_prompt):
    from app import model   
    print("aqui se ejecuto dentro de sam_get_mas_and 2")
    prompt = get_prompt(point_prompt)
    
    print("aqui despues de get_prompt")
    index = prompt["index"]
    print("aqui despues de index ", index)

    ruta_original,ruta_copy, ruta_mask  = obtener_ruta_frame(videoId, index)
    print(ruta_mask)
    print("aqui antes de ruta")
    img = cv2.imread(ruta_original[0])
    # ruta_img, ruta_copy, ruta_mask=resultado

    print("aqui se ejecuto antes del metodo predictor 4")

    imagen, mask = model.predict(img , prompt)
    print("despues de predictor")
    guardar_imagen_modificada(ruta_copy[0] , imagen)
    guardar_imagen_modificada(ruta_mask[0] , mask)
    # guardar_imagen_modificada(ruta_mask,mask)

    print("imagen modificada guardada")
    return ruta_mask





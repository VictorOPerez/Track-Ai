
from resources.get_prompt import get_prompt
from db.consultaDb import obtener_ruta_frame
from db.funcionesDb import guardar_imagen_modificada
import numpy as np

def sam_get_mask_and_refine(videoId, point_prompt):
    from app import model   
    print("aqui se ejecuto dentro de sam_get_mas_and 2")
    prompt = get_prompt(point_prompt)
    
    index =prompt["index"]
    ruta_img, ruta_copy, ruta_mask= obtener_ruta_frame(videoId,index)

    print("aqui se ejecuto antes del metodo predictor 4")

    imagen, mask = model.predict(ruta_copy , prompt)
    guardar_imagen_modificada(ruta_copy , imagen)
    guardar_imagen_modificada(ruta_mask,mask)

    print("imagen modificada guardada")
    return ruta_copy, ruta_mask





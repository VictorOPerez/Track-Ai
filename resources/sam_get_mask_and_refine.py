
from resources.get_prompt import get_prompt
import numpy as np

def sam_get_mask_and_refine(video_state, point_prompt):
    from app import model   
    print("aqui se ejecuto dentro de sam_get_mas_and 2")
    prompt = get_prompt(point_prompt)
    
    print("aqui se ejecuto antes de index")
    index =prompt["index"]
    print("aqui se ejecuto despues de index")
    print(video_state,"VALOR DE VIDEO_STATE")
    print(index,type(index),"VALOR DE INDEX")
    image  = video_state["fcopy"][index]
    print("aqui despues de imagen")

    print("aqui se ejecuto antes del metodo predictor 4")
    imagen, mask = model.predict(image,prompt)

    video_state["masks"][index]= mask
    video_state["fcopy"][index]= imagen

    return imagen, video_state, index



from app import model
from get_prompt import get_prompt
import numpy as np

def sam_get_mask_and_refine(video_state, point_prompt):

    prompt = get_prompt(point_prompt)
    
    index =prompt["index"]
    image  = video_state["fcopy"][index]

    imagen, mask = model.predict(image,prompt)

    video_state["masks"][index]= mask
    video_state["fcopy"][index]= imagen

    return imagen, video_state, index


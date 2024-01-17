import json
import numpy as np

# convert points input to prompt state
def get_prompt(puntos):
    # Convierte la cadena de entrada 'click_input', que está en formato JSON, en un objeto Python.
    print(puntos)
    input= puntos["puntos"]
    print(input)

    # Extrae los puntos y etiquetas actuales del estado del clic.
    # points = click_state[0]
    # labels = click_state[1]

    points=[]
    points_label=[]

    for inp in input:
        # print(inp["x"])
        points.append([inp["x"],inp["y"]])
        points_label.append(1)
        # points.append= inp["frameAct"]

   
    prompt = {
        "point":np.array(points) ,  # Lista de puntos de clic actualizados.
        "label": np.array(points_label),  # Lista de etiquetas asociadas a cada punto de clic. 
         "index": input[0]["frameAct"] #frame actual
    }

    # # Devuelve el diccionario 'prompt' actualizado.
    return prompt

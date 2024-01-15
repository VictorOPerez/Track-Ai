import json

# convert points input to prompt state
def get_prompt(click_state, click_input):
    # Convierte la cadena de entrada 'click_input', que está en formato JSON, en un objeto Python.
    inputs = json.loads(click_input)

    # Extrae los puntos y etiquetas actuales del estado del clic.
    points = click_state[0]
    labels = click_state[1]

    # Itera sobre cada entrada en 'inputs'.
    for input in inputs:
        # Añade las coordenadas del punto (primeros dos elementos de 'input') a 'points'.
        points.append(input[:2])
        # Añade la etiqueta (tercer elemento de 'input') a 'labels'.
        labels.append(input[2])

    # Actualiza el estado del clic con los nuevos puntos y etiquetas.
    click_state[0] = points
    click_state[1] = labels

    # Crea un diccionario 'prompt' con información sobre el tipo de entrada,
    # los puntos de clic y las etiquetas, y una bandera para la salida multimáscara.
    prompt = {
        "prompt_type": ["click"],  # Tipo de acción realizada.
        "input_point": click_state[0],  # Lista de puntos de clic actualizados.
        "input_label": click_state[1],  # Lista de etiquetas asociadas a cada punto de clic.
        "multimask_output": "True",  # Indica si se espera una salida de multimáscara.
    }

    # Devuelve el diccionario 'prompt' actualizado.
    return prompt

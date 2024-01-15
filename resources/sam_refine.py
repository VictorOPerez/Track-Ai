
from app import model
from get_prompt import get_prompt
import numpy as np

def sam_refine(video_state, point_prompt, click_state, interactive_state, evt:gr.SelectData):
    """
    Esta función refina una imagen de un video basándose en entradas de clics positivos o negativos.

    Args:
        video_state: Estado actual del video, incluyendo información sobre los fotogramas y otros metadatos.
        point_prompt: Indicador de si el clic es positivo o negativo.
        click_state: Estado actual de los clics, incluyendo puntos y etiquetas.
        interactive_state: Estado interactivo que lleva registro de la interacción del usuario.
        evt: Datos seleccionados por el usuario, generalmente coordenadas de clic.
    """
    # Determina si el clic es positivo o negativo y actualiza el estado interactivo.
    if point_prompt == "Positive":
        coordinate = "[[{},{},1]]".format(evt.index[0], evt.index[1])
        interactive_state["positive_click_times"] += 1
    else:
        coordinate = "[[{},{},0]]".format(evt.index[0], evt.index[1])
        interactive_state["negative_click_times"] += 1
    
    # Reinicia y establece la imagen en el controlador del modelo SAM.
    model.samcontroler.sam_controler.reset_image()
    model.samcontroler.sam_controler.set_image(video_state["origin_images"][video_state["select_frame_number"]])

    # Obtiene un prompt (instrucción) actualizado con base en el estado de los clics y la nueva coordenada.
    prompt = get_prompt(click_state=click_state, click_input=coordinate)

    # Utiliza el modelo SAM para refinar la imagen basándose en los clics.
    mask, logit, painted_image = model.first_frame_click( 
                                                      image=video_state["origin_images"][video_state["select_frame_number"]], 
                                                      points=np.array(prompt["input_point"]),
                                                      labels=np.array(prompt["input_label"]),
                                                      multimask=prompt["multimask_output"]
                                                      )

    # Actualiza el estado del video con la nueva máscara, logits y la imagen pintada.
    video_state["masks"][video_state["select_frame_number"]] = mask
    video_state["logits"][video_state["select_frame_number"]] = logit
    video_state["painted_images"][video_state["select_frame_number"]] = painted_image
    # Crea un registro de operaciones para el proceso de refinamiento.
    operation_log = [("",""), ("Use SAM for segment. You can try add positive and negative points by clicking. Or press Clear clicks button to refresh the image. Press Add mask button when you are satisfied with the segment","Normal")]

    # Devuelve la imagen pintada, el estado actualizado del video, el estado interactivo y el registro de operaciones.
    return painted_image, video_state, interactive_state, operation_log


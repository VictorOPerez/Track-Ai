import time
import cv2
import psutil
import os
import numpy as np
from app import model
import torch 
import torchvision
from tools.painter import mask_painter


def clear_click(video_state, click_state):
    """
    Limpia el historial de clics y refresca la imagen actual del video.

    Args:
        video_state: El estado actual del video, incluyendo información sobre los fotogramas.
        click_state: El estado actual de los clics realizados por el usuario.

    Returns:
        template_frame: El fotograma actual del video sin modificaciones.
        click_state: El estado de los clics reseteado.
        operation_log: Registro de operaciones realizadas.
    """

    # Reinicia el estado de los clics a listas vacías.
    click_state = [[], []]

    # Obtiene el fotograma actual del video que está siendo editado o visualizado.
    template_frame = video_state["origin_images"][video_state["select_frame_number"]]

    # Crea un registro de operaciones indicando que los puntos y la imagen han sido refrescados.
    operation_log = [("",""), ("Clear points history and refresh the image.", "Normal")]

    # Devuelve el fotograma actual sin cambios, el estado de clics reseteado y el registro de operaciones.
    return template_frame, click_state, operation_log


def remove_multi_mask(interactive_state, mask_dropdown):
    """
    Limpia todas las máscaras almacenadas en el estado interactivo.

    Args:
        interactive_state: El estado interactivo actual que almacena información sobre las máscaras y otros elementos.
        mask_dropdown: Una lista de selección de máscaras (no se utiliza en esta función).

    Returns:
        interactive_state: El estado interactivo actualizado después de eliminar las máscaras.
    """

    # Vacía la lista de nombres de máscaras en el estado interactivo.
    interactive_state["multi_mask"]["mask_names"] = []

    # Vacía la lista de máscaras en el estado interactivo.
    interactive_state["multi_mask"]["masks"] = []

    # Crea un registro de operaciones que indica que todas las máscaras han sido eliminadas.
    operation_log = [("",""), ("Remove all mask, please add new masks", "Normal")]

    # Devuelve el estado interactivo actualizado.
    return interactive_state


def show_mask(video_state, interactive_state, mask_dropdown):
    """
    Visualiza las máscaras seleccionadas en un fotograma del video.

    Args:
        video_state: Estado actual del video, incluyendo información sobre los fotogramas.
        interactive_state: Estado interactivo que incluye información sobre las máscaras.
        mask_dropdown: Lista de máscaras seleccionadas para visualizar.

    Returns:
        select_frame: El fotograma del video con las máscaras aplicadas.
        operation_log: Registro de operaciones realizadas.
    """

    # Ordena las máscaras seleccionadas para mantener una consistencia.
    mask_dropdown.sort()

    # Obtiene el fotograma actual del video que se está visualizando o editando.
    select_frame = video_state["origin_images"][video_state["select_frame_number"]]

    # Itera sobre cada máscara seleccionada en mask_dropdown.
    for i in range(len(mask_dropdown)):
        # Obtiene el número de la máscara de la lista desplegable.
        mask_number = int(mask_dropdown[i].split("_")[1]) - 1

        # Obtiene la máscara específica del estado interactivo.
        mask = interactive_state["multi_mask"]["masks"][mask_number]

        # Aplica la máscara al fotograma seleccionado.
        select_frame = mask_painter(select_frame, mask.astype('uint8'), mask_color=mask_number + 2)
    
    # Crea un registro de operaciones que indica las máscaras seleccionadas para seguimiento o inpainting.
    operation_log = [("",""), ("Select {} for tracking or inpainting".format(mask_dropdown), "Normal")]

    # Devuelve el fotograma con las máscaras aplicadas y el registro de operaciones.
    return select_frame, operation_log


# get the select frame from gradio slider
def select_template(image_selection_slider, video_state, interactive_state, mask_dropdown):
    """
    Selecciona un fotograma específico del video como plantilla para operaciones posteriores.

    Args:
        image_selection_slider: Índice del fotograma seleccionado por el usuario.
        video_state: Estado actual del video, incluyendo información sobre los fotogramas.
        interactive_state: Estado interactivo que incluye información sobre las interacciones del usuario.
        mask_dropdown: Lista de máscaras seleccionadas (no utilizada directamente en esta función).

    Returns:
        El fotograma pintado seleccionado, el estado actualizado del video, el estado interactivo y el registro de operaciones.
    """

    # Ajusta el índice del fotograma seleccionado restando 1, ya que los índices en Python comienzan en 0.
    image_selection_slider -= 1

    # Actualiza el número del fotograma seleccionado en el estado del video.
    video_state["select_frame_number"] = image_selection_slider

    # Reinicia y establece la imagen en el controlador del modelo SAM.
    model.samcontroler.sam_controler.reset_image()
    model.samcontroler.sam_controler.set_image(video_state["origin_images"][image_selection_slider])

    # Comprueba si hay máscaras seleccionadas. Este bloque parece estar en desarrollo o para depuración.
    if mask_dropdown:
        print("ok")

    # Crea un registro de operaciones indicando que se ha seleccionado un nuevo fotograma.
    operation_log = [("",""), ("Select frame {}. Try click image and add mask for tracking.".format(image_selection_slider), "Normal")]

    # Devuelve el fotograma pintado seleccionado, el estado actualizado del video, el estado interactivo y el registro de operaciones.
    return video_state["painted_images"][image_selection_slider], video_state, interactive_state, operation_log


def get_resize_ratio(resize_ratio_slider, interactive_state):
    """
    Actualiza la relación de tamaño (resize ratio) en el estado interactivo.

    Args:
        resize_ratio_slider: Valor actual del control deslizante de relación de tamaño seleccionado por el usuario.
        interactive_state: Estado interactivo actual de la aplicación.

    Returns:
        El estado interactivo actualizado con la nueva relación de tamaño.
    """

    # Actualiza el estado interactivo con el nuevo valor de la relación de tamaño.
    interactive_state["resize_ratio"] = resize_ratio_slider

    # Devuelve el estado interactivo actualizado.
    return interactive_state


# set the tracking end frame
def get_end_number(track_pause_number_slider, video_state, interactive_state):
    """
    Actualiza el estado interactivo con un número de fotograma que marca el fin del seguimiento.

    Args:
        track_pause_number_slider: El número de fotograma seleccionado por el usuario como el fin del seguimiento.
        video_state: Estado actual del video, incluyendo información sobre los fotogramas.
        interactive_state: Estado interactivo actual de la aplicación.

    Returns:
        El fotograma pintado correspondiente al número de fin del seguimiento, el estado interactivo actualizado y el registro de operaciones.
    """

    # Actualiza el estado interactivo con el número de fotograma seleccionado como el fin del seguimiento.
    interactive_state["track_end_number"] = track_pause_number_slider

    # Crea un registro de operaciones que indica el número de fotograma seleccionado para finalizar el seguimiento.
    operation_log = [("",""), ("Set the tracking finish at frame {}".format(track_pause_number_slider), "Normal")]

    # Devuelve el fotograma pintado correspondiente al número de fin del seguimiento, junto con el estado interactivo actualizado y el registro de operaciones.
    return video_state["painted_images"][track_pause_number_slider], interactive_state, operation_log

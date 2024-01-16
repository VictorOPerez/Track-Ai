from useful_tools import show_mask

def add_multi_mask(video_state, interactive_state, mask_dropdown):
    """
    Agrega una nueva máscara al estado interactivo y actualiza la lista desplegable de máscaras.

    Args:
        video_state: Estado actual del video, incluyendo información sobre los fotogramas y las máscaras.
        interactive_state: Estado interactivo que incluye información sobre las máscaras y otros elementos.
        mask_dropdown: Lista desplegable de las máscaras disponibles para el usuario.

    Returns:
        El estado interactivo actualizado con la nueva máscara añadida.
    """

    try:
        # Obtiene la máscara del fotograma seleccionado actualmente.
        mask = video_state["masks"][video_state["select_frame_number"]]

        # Añade la máscara al estado interactivo.
        interactive_state["multi_mask"]["masks"].append(mask)

        # Añade un nombre único para la nueva máscara en el estado interactivo y en la lista desplegable.
        new_mask_name = "mask_{:03d}".format(len(interactive_state["multi_mask"]["masks"]))
        interactive_state["multi_mask"]["mask_names"].append(new_mask_name)
        mask_dropdown.append(new_mask_name)

        # Muestra la máscara en el fotograma seleccionado y obtiene el estado de ejecución.
        select_frame, run_status = show_mask(video_state, interactive_state, mask_dropdown)

        # Crea un registro de operaciones que indica que se ha añadido una nueva máscara.
        operation_log = [("",""),("Added a mask, use the mask select for target tracking or inpainting.","Normal")]
    except:
        # En caso de error (por ejemplo, si no hay una máscara generada), registra un mensaje de error.
        operation_log = [("Please click the left image to generate mask.", "Error"), ("","")]

    # Devuelve el estado interactivo actualizado.
    return interactive_state

import numpy as np
from app import model
from generate_video_from_frames import generate_video_from_frames
# inpaint 

def inpaint_video(video_state, interactive_state, mask_dropdown):
    # Inicializa un registro de operaciones para el proceso de inpainting (relleno).
    operation_log = [("",""), ("Removed the selected masks.", "Normal")]

    # Convierte la lista de fotogramas originales a un array de NumPy.
    frames = np.asarray(video_state["origin_images"])

    # Obtiene la tasa de fotogramas por segundo (fps) del video.
    fps = video_state["fps"]

    # Convierte la lista de máscaras a un array de NumPy.
    inpaint_masks = np.asarray(video_state["masks"])

    # Si no hay máscaras seleccionadas, se establece una máscara predeterminada.
    if len(mask_dropdown) == 0:
        mask_dropdown = ["mask_001"]
    mask_dropdown.sort()

    # Convierte las selecciones de máscaras del dropdown a números de máscara.
    inpaint_mask_numbers = [int(mask.split("_")[1]) for mask in mask_dropdown]

    # Itera sobre todas las máscaras únicas y elimina las que no están en mask_dropdown.
    unique_masks = np.unique(inpaint_masks)
    num_masks = len(unique_masks) - 1
    for i in range(1, num_masks + 1):
        if i not in inpaint_mask_numbers:
            inpaint_masks[inpaint_masks == i] = 0

    # Intenta realizar el inpainting en los fotogramas del video usando las máscaras seleccionadas.
    try:
        inpainted_frames = model.baseinpainter.inpaint(frames, inpaint_masks, ratio=interactive_state["resize_ratio"])
    except:
        # Registra un error si el inpainting falla, por ejemplo, por falta de máscaras o exceso de uso de VRAM.
        operation_log = [("Error! You are trying to inpaintwithout masks input. Please track the selected mask first, and then press inpaint. If VRAM exceeded, please use the resize ratio to scaling down the image size.", "Error"), ("", "")]

    # En caso de error, se mantienen los fotogramas originales sin cambios.
    inpainted_frames = video_state["origin_images"]
    # Genera un video a partir de los fotogramas inpintados y lo guarda en una ruta específica.
    video_output = generate_video_from_frames(inpainted_frames, output_path="./result/inpaint/{}".format(video_state["video_name"]), fps=fps)

    # Devuelve el video generado y el registro de operaciones.
    return video_output, operation_log

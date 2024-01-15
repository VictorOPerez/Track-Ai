
import time
import cv2
import psutil
import os
import numpy as np
from app import model
from generate_video_from_frames import generate_video_from_frames


def vos_tracking_video(video_state, interactive_state, mask_dropdown):
    # Inicializa un registro de operaciones para el seguimiento de acciones y mensajes.
    operation_log = [("",""), ("Track the selected masks, and then you can select the masks for inpainting.","Normal")]

    # Limpia la memoria del modelo, presumiblemente para optimizar el rendimiento y liberar recursos.
    model.xmem.clear_memory()

    # Selecciona los fotogramas del video que serán procesados, basándose en el estado interactivo actual.
    if interactive_state["track_end_number"]:
        following_frames = video_state["origin_images"][video_state["select_frame_number"]:interactive_state["track_end_number"]]
    else:
        following_frames = video_state["origin_images"][video_state["select_frame_number"]:]

    # Procesa las máscaras seleccionadas para realizar el seguimiento.
    if interactive_state["multi_mask"]["masks"]:
        # Si no hay máscaras seleccionadas, se establece una máscara predeterminada.
        if len(mask_dropdown) == 0:
            mask_dropdown = ["mask_001"]
        mask_dropdown.sort()
        # Crea una máscara combinada a partir de las máscaras seleccionadas.
        template_mask = interactive_state["multi_mask"]["masks"][int(mask_dropdown[0].split("_")[1]) - 1] * (int(mask_dropdown[0].split("_")[1]))
        for i in range(1, len(mask_dropdown)):
            mask_number = int(mask_dropdown[i].split("_")[1]) - 1 
            template_mask = np.clip(template_mask + interactive_state["multi_mask"]["masks"][mask_number] * (mask_number + 1), 0, mask_number + 1)
        video_state["masks"][video_state["select_frame_number"]] = template_mask
    else:      
        # Si no hay nuevas máscaras seleccionadas, utiliza la máscara existente en el estado del video.
      template_mask = video_state["masks"][video_state["select_frame_number"]]
      # Obtiene la tasa de fotogramas por segundo (fps) del video del estado del video.
      fps = video_state["fps"]

    # Verifica si hay un error en la operación, como una máscara única sin variación.
    if len(np.unique(template_mask)) == 1:
        # Modifica ligeramente la máscara para evitar un error y actualiza el registro de operaciones.
        template_mask[0][0] = 1
        operation_log = [("Error! Please add at least one mask to track by clicking the left image.", "Error"), ("", "")]

    # Utiliza el modelo para generar las máscaras, logits (probablemente probabilidades o puntuaciones de clase) y las imágenes pintadas (procesadas) basadas en los fotogramas y la máscara de plantilla.
    masks, logits, painted_images = model.generator(images=following_frames, template_mask=template_mask)

    # Limpia nuevamente la memoria del GPU para liberar recursos.
    model.xmem.clear_memory()    

    if interactive_state["track_end_number"]: 
    # Actualiza el estado del video con las nuevas máscaras, logits y las imágenes pintadas hasta el número de fotograma especificado.
        video_state["masks"][video_state["select_frame_number"]:interactive_state["track_end_number"]] = masks
        video_state["logits"][video_state["select_frame_number"]:interactive_state["track_end_number"]] = logits
        video_state["painted_images"][video_state["select_frame_number"]:interactive_state["track_end_number"]] = painted_images
    else:
        # Actualiza el estado del video con las nuevas máscaras, logits y las imágenes pintadas desde el fotograma seleccionado hasta el final.
        video_state["masks"][video_state["select_frame_number"]:] = masks
        video_state["logits"][video_state["select_frame_number"]:] = logits
        video_state["painted_images"][video_state["select_frame_number"]:] = painted_images

    # Genera un video a partir de las imágenes pintadas y lo guarda en una ruta específica.
    video_output = generate_video_from_frames(video_state["painted_images"], output_path="./result/track/{}".format(video_state["video_name"]), fps=fps)

    # Incrementa el contador de veces de inferencia en el estado interactivo.
    interactive_state["inference_times"] += 1

    # Imprime información sobre el número de inferencias, clics y clasificaciones de clics durante el proceso.
    print("For generating this tracking result, inference times: {}, click times: {}, positive: {}, negative: {}".format(interactive_state["inference_times"], 
                                                                                                                        interactive_state["positive_click_times"]+interactive_state["negative_click_times"],
                                                                                                                        interactive_state["positive_click_times"],
                                                                                                                        interactive_state["negative_click_times"]))

    # Código para guardar las máscaras generadas si se activa la opción correspondiente.
    if interactive_state["mask_save"]:
        # Verifica si el directorio para guardar las máscaras existe, si no, lo crea.
        if not os.path.exists('./result/mask/{}'.format(video_state["video_name"].split('.')[0])):
            os.makedirs('./result/mask/{}'.format(video_state["video_name"].split('.')[0]))
        i = 0
        print("save mask")
        # Guarda cada máscara en el directorio especificado.
        for mask in video_state["masks"]:
            np.save(os.path.join('./result/mask/{}'.format(video_state["video_name"].split('.')[0]), '{:05d}.npy'.format(i)), mask)
            i += 1

    # Devuelve el video generado, el estado actualizado del video, el estado interactivo y el registro de operaciones.
    return video_output, video_state, interactive_state,operation_log

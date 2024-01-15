import time
import cv2
import psutil
import os
import numpy as np
from app import model
import torch 
import torchvision

def generate_video_from_frames(frames, output_path, fps=30):
    """
    Genera un video a partir de una lista de fotogramas.

    Args:
        frames (list of numpy arrays): Los fotogramas a incluir en el video.
        output_path (str): La ruta donde se guardará el video generado.
        fps (int, optional): La tasa de fotogramas del video de salida. Por defecto es 30.
    """

    # Convertir la lista de fotogramas (numpy arrays) en un tensor de PyTorch.
    # Esto es necesario para la función write_video de torchvision.
    frames = torch.from_numpy(np.asarray(frames))

    # Comprueba si el directorio donde se guardará el video existe.
    # Si no existe, lo crea.
    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))

    # Utiliza la función write_video de torchvision para crear y guardar el video.
    # Se especifica el codec de video 'libx264' para la compresión.
    torchvision.io.write_video(output_path, frames, fps=fps, video_codec="libx264")

    # Devuelve la ruta del archivo de video generado.
    return output_path

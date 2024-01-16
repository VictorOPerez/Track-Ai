import gradio as gr
import argparse
import gdown
import cv2
import numpy as np
import os
import sys
sys.path.append(sys.path[0]+"/tracker")
sys.path.append(sys.path[0]+"/tracker/model")
import requests
import json
import torchvision
import torch 
from tools.painter import mask_painter
import psutil
import time
from resources.get_frames_from_video import get_frames_from_video
from resources.sam_get_mask_and_refine import sam_get_mask_and_refine
from flask_cors import CORS
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify


try: 
    from mmcv.cnn import ConvModule
except:
    os.system("mim install mmcv")

from resources.Download import Download
from track_anything import TrackingAnything
from track_anything import parse_augment

args = parse_augment()
args.port = 12212
args.device = "cuda:3"
# args.mask_save = True
SAM_checkpoint,xmem_checkpoint,e2fgvi_checkpoint =Download()

# initialize sam, xmem, e2fgvi model
model = TrackingAnything(SAM_checkpoint, xmem_checkpoint, e2fgvi_checkpoint,args)



app = Flask(__name__)
CORS(app, supports_credentials=True)

# CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})


app.config['UPLOAD_FOLDER'] = 'uploads'

video={}


@app.route('/')
def index():
    response_data = {
    "status": "success",
    "message": "Hola mundo",
    }
    return jsonify(response_data)
    
@app.route('/api/upload_video', methods=['POST'])
def upload_file():
    global video
    if 'video' not in request.files:
        return 'No video part'
    file = request.files['video']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        cap = cv2.VideoCapture(file_path)  # Intenta abrir el video para la lectura de fotogramas.
        fps = cap.get(cv2.CAP_PROP_FPS) 
        video= get_frames_from_video(file_path)
        # print(video)
        response_data = {
      "status": "success",
      "fps": fps,
      }

      
        return jsonify(response_data)
    

    
@app.route('/api/addMask', methods=['POST'])
def addMask():
    global video
    # print(video)
    try:
        # Obtiene el JSON de la solicitud,
        data = request.get_json()
        # print(data)
        sam_get_mask_and_refine(video,data)
        # Comprueba si se recibió un JSON válido
        if data is not None:
            # data ahora es un diccionario de Python
            # Puedes trabajar con los datos como un diccionario
            return jsonify({"message": "JSON recibido correctamente", "data": data}), 200
        else:
            return jsonify({"message": "No se recibió JSON válido"}), 400

    except Exception as e:
        return jsonify({"message": "Error al procesar JSON", "error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)


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
from Track_Any import Track_Any
from track_anything import parse_augment

args = parse_augment()
args.port = 12212
args.device = "cuda"
# args.mask_save = True
SAM_checkpoint,xmem_checkpoint,e2fgvi_checkpoint =Download()

# initialize sam, xmem, e2fgvi model
model = Track_Any(SAM_checkpoint, xmem_checkpoint, e2fgvi_checkpoint,args)



app = Flask(__name__)
CORS(app, supports_credentials=True)

# CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})


app.config['UPLOAD_FOLDER'] = 'uploads'


@app.route('/')
def index():
    response_data = {
    "status": "success",
    "message": "Hola mundo",
    }
    return jsonify(response_data)
    
@app.route('/api/upload_video', methods=['POST'])
def upload_file():

    if 'video' not in request.files:
        return 'No video part'
    file = request.files['video']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        fps = get_frames_from_video(file_path)

        response_data = {
      "status": "success",
      "fps": fps,
      }

      
        return jsonify(response_data)
    

    
@app.route('/api/addMask', methods=['POST'])
def addMask():
    try:
        # Obtiene el JSON de la solicitud,
        dataPuntos = request.get_json()
        # print(data)
        print("AQUI SE EJECUTO 1")
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], "Download_2.mp4")
        # video= get_frames_from_video(file_path)
        videoId=2
        ruta_copy, ruta_mask = sam_get_mask_and_refine(videoId,dataPuntos)
        print("imagen guardada con exito")
        if dataPuntos is not None:
            return jsonify({"message": "JSON recibido correctamente", "data": dataPuntos}), 200
        else:
            return jsonify({"message": "No se recibió JSON válido"}), 400

    except Exception as e:
        return jsonify({"message": "Error al procesar JSON", "error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=3000, host="0.0.0.0")


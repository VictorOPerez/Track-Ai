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





import PIL
from tqdm import tqdm

from tools.Sam_segment import Sam_segment
from tracker.base_tracker import BaseTracker
from inpainter.base_inpainter import BaseInpainter
import numpy as np
import argparse


class Track_Any():
    def __init__(self, sam_checkpoint, xmem_checkpoint, e2fgvi_checkpoint, args):
        self.args = args
        self.sam_checkpoint = sam_checkpoint
        self.xmem_checkpoint = xmem_checkpoint
        self.e2fgvi_checkpoint = e2fgvi_checkpoint
        self.samcontroler = Sam_segment(self.sam_checkpoint, args.sam_model_type, args.device)
        self.xmem = BaseTracker(self.xmem_checkpoint, device=args.device)
        self.baseinpainter = BaseInpainter(self.e2fgvi_checkpoint, args.device) 
 
    def predict(self,  image, prompts):
        print("aqui se ejecuto dentro de el metodo predictor 5")
        imagePaited, masks= self.samcontroler.predict(image, prompts)
        return  imagePaited, masks

    def generator(self, images: list, template_mask:np.ndarray):
        
        masks = []
        logits = []
        painted_images = []
        for i in tqdm(range(len(images)), desc="Tracking image"):
            if i ==0:           
                mask, logit, painted_image = self.xmem.track(images[i], template_mask)
                masks.append(mask)
                logits.append(logit)
                painted_images.append(painted_image)
                
            else:
                mask, logit, painted_image = self.xmem.track(images[i])
                masks.append(mask)
                logits.append(logit)
                painted_images.append(painted_image)
        return masks, logits, painted_images
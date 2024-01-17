from segment_anything import sam_model_registry, SamPredictor, SamAutomaticMaskGenerator
import torch
import numpy as np
from .painter import mask_painter, point_painter



class Sam_segment:
    def __init__(self, SAM_checkpoint, model_type, device='cuda:0'):
        """
        device: model device
        SAM_checkpoint: path of SAM checkpoint
        model_type: vit_b, vit_l, vit_h
        """
        print(f"Initializing BaseSegmenter to {device}")
        assert model_type in ['vit_b', 'vit_l', 'vit_h'], 'model_type must be vit_b, vit_l, or vit_h'

        self.device = device
        self.torch_dtype = torch.float16 if 'cuda' in device else torch.float32
        self.model = sam_model_registry[model_type](checkpoint=SAM_checkpoint)
        self.model.to(device=self.device)
        self.predictor = SamPredictor(self.model)
        self.embedded = False
    
    @torch.no_grad()
    def reset_image(self):
        # reset image embeding
        self.predictor.reset_image()
        self.embedded = False

    def predict(self, image, prompts):
               
        self.predictor.set_image(image)
        
        masks, _, _ = self.predictor.predict(
                                              point_coords=prompts["point"],
                                              point_labels=prompts["label"],
                                              multimask_output=False,
                                          )
        
        imagePaited = mask_painter(image,masks)
        # imagen pintada
        
        return imagePaited, masks

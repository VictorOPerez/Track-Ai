from segment_anything import sam_model_registry, SamPredictor, SamAutomaticMaskGenerator
import torch
import numpy as np
from .mask_painter import mask_painter



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
        print("aqui se ejecuto dentro de la Clase Sam_segment 6")

        masks, scores, _ = self.predictor.predict(
                                              point_coords=prompts["point"],
                                              point_labels=prompts["label"],
                                              multimask_output=False,
                                          )
        print("aqui se ejecuto dentro de la Clase Sam_segment se optuvo la prediccion 7")

        imagePaited = mask_painter(image, masks[np.argmax(scores)].astype('uint8'))
        # imagen pintada
        print("aqui se ejecuto dentro de la Clase Sam_segment se optuvo la imagen pintada 7")
        
        return imagePaited, masks

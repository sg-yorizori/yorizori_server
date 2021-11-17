import os
import torch
from PIL import Image

class Dectect_Ingrd:
    def __init__(self):
        dir_path = os.getcwd()
        pt_path = os.path.join(dir_path, 'ingrd_yolov5m_best.pt')
        model = torch.hub.load('ultralytics/yolov5', 'custom', path=pt_path)

    def detect(self, img_path):
        img = Image.open(img_path)
        results = self.model(img)
        # index / xmin / ymin / xmax / ymax / confidence / class / name
        return results.pandas().xyxy[0].sort_values('xmin')  # sorted left-right

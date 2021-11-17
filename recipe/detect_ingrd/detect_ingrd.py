import os
import torch
from PIL import Image
from download_pt import download_file_from_google_drive

class Dectect_Ingrd:
    def __init__(self, pt='last'):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        last_pt_path = os.path.join(dir_path, 'ingrd_yolov5m_last.pt')
        best_pt_path = os.path.join(dir_path, 'ingrd_yolov5m_best.pt')

        if pt == 'best':    
            pt = best_pt_path
            pt_file_id = '1hKzz9biYDxk7HJozX05esTEuot7YUPse'
        else:
            pt = last_pt_path
            pt_file_id = '1faMy4fwzHAmvOkvH_-Y4AkNSCTjAjh87'
        
        if not os.path.exists(pt):
            print('download pt from google drive...')
            download_file_from_google_drive(pt_file_id, pt)
            print('download complete!')

        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=pt)

    def detect(self, img_path):
        img = Image.open(img_path)
        results = self.model(img)
        # index / xmin / ymin / xmax / ymax / confidence / class / name
        return results

if __name__ == "__main__":
    detection = Dectect_Ingrd() #Dectect_Ingrd('best')
    results = detection.detect("E:/test.jpg") #for test

    # results.print()
    # results.save()
    print(results.pandas().xyxy[0].to_json(orient="records")) #to json format
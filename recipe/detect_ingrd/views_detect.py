from rest_framework.response import Response
from rest_framework.views import APIView
from recipe.models import Ingredients
from recipe.serializers import IngredientsSerializer

from recipe.detect_ingrd.model import *
import base64
import numpy as np
import cv2
import os
import os.path as osp


class DetectIngrdViewAPI(APIView):
    detection = Dectect_Ingrd()

    def post(self, request):
        base64Image = request.data['image']
        base64Image = encodebase64(base64Image)

        target_folder = osp.join(os.getcwd(), 'target')
        target_path = osp.join(os.getcwd(), 'target/target.jpg')
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
        cv2.imwrite(target_path, base64Image)

        # target image detect
        #detection = Dectect_Ingrd()
        _, img_result = self.detection.detect(target_path)

        # result image
        # img_result == result/target.jpg
        img_result = decodebase64(img_result)

        # detect ingrd list
        detect_list = self.detection.get_result_ingrd_list()
        detect_set = list(set(detect_list))

        Ingredient_List = Ingredients.objects.filter(name__in=detect_set)
        serializers = IngredientsSerializer(Ingredient_List, many=True)

        return Response({"ingrd": serializers.data, "result": img_result})


def encodebase64(data):
    imageStr = base64.b64decode(data)
    nparr = np.fromstring(imageStr, np.uint8)
    base64Image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return base64Image


def decodebase64(image):
    with open(image, 'rb') as img:
        base64Image = base64.b64encode(img.read())
    return base64Image

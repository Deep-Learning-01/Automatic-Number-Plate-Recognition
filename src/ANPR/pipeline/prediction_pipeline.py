import os, sys
import numpy as np
from src.ANPR.logger import logging
from src.ANPR.exception import ANPRException
from src.ANPR.entity.config_entity import *
import cv2
import matplotlib.pyplot as plt
import tensorflow as tf
from keras.utils.image_utils import load_img, img_to_array
from PIL import Image

BASE_PATH = os.getcwd()
UPLOAD_PATH = os.path.join(BASE_PATH, 'artifacts','Training','model.h5' )
model = tf.keras.models.load_model(UPLOAD_PATH)

image= 'E:\INEURON_DATA\CV\Automatic-Number-Plate-Recognition\notebooks\TEST\car.jpeg'

class ModelPredictor:
    def __init__(self):
        pass

    def object_detection(self,path, filename):
        # Read image
        image = load_img(path)  # PIL object
        image = np.array(image, dtype=np.uint8)  # 8 bit array (0,255)
        image1 = load_img(path, target_size=(224, 224))
        # Data preprocessing
        # Convert into array and get the normalized output
        image_arr_224 = img_to_array(image1)/255.0
        h, w, d = image.shape
        test_arr = image_arr_224.reshape(1, 224, 224, 3)
        # Make predictions
        coords = model.predict(test_arr)
        # Denormalize the values
        denorm = np.array([w, w, h, h])
        coords = coords * denorm
        coords = coords.astype(np.int32)
        # Draw bounding on top the image
        xmin, xmax, ymin, ymax = coords[0]
        pt1 = (xmin, ymin)
        pt2 = (xmax, ymax)
        print(pt1, pt2)
        cv2.rectangle(image, pt1, pt2, (0, 255, 0), 3)
        # Convert into bgr
        image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        cv2.imwrite(
            'E:/INEURON_DATA/CV/Automatic-Number-Plate-Recognition/static/predict/{}'.format(filename), image_bgr)
        return coords

    def OCR(self,path, filename):
        img = np.array(load_img(path))
        cods = self.object_detection(path, filename)
        xmin, xmax, ymin, ymax = cods[0]
        roi = img[ymin:ymax, xmin:xmax]
        roi_bgr = cv2.cvtColor(roi, cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(roi_bgr, cv2.COLOR_BGR2GRAY)
        #magic_color = self.apply_brightness_contrast(gray, brightness=40, contrast=70)
        cv2.imwrite(
            'E:/INEURON_DATA/CV/Automatic-Number-Plate-Recognition/static/roi/{}'.format(filename), roi_bgr)

        text = "Satya Thakur"
        
        return text

    def apply_brightness_contrast(self,input_img, brightness=0, contrast=0):

        if brightness != 0:
            if brightness > 0:
                shadow = brightness
                highlight = 255
            else:
                shadow = 0
                highlight = 255 + brightness
            alpha_b = (highlight - shadow)/255
            gamma_b = shadow

            buf = cv2.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
        else:
            buf = input_img.copy()

        if contrast != 0:
            f = 131*(contrast + 127)/(127*(131-contrast))
            alpha_c = f
            gamma_c = 127*(1-f)

            buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)

        return buf
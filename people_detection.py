import yolo3_one_file_to_detect_them_all as yolo
from tensorflow.keras.models import load_model
import numpy as np
from numpy import expand_dims
from PIL import Image
from keras.preprocessing.image import img_to_array
from matplotlib import pyplot
from video_frame import VideoFrame
from bounding_box import BoundingBox

class PeopleDetector:
    """
    People detection with YOLO.
    Attributes
    ---------- 
        model : keras model
            YOLOv3
    """

    def __init__(self):
        self.model = load_model('model.h5')

    def load_image_pixels(self, image, shape = (512,512)):
        """ kép + modell számára elvárt méret -> előfeldolgozott kép + eredeti méret """

        height, width, _= image.shape
        image = Image.fromarray(image)
        image = image.resize(shape)
        image = img_to_array(image)
        image = image.astype('float32')
        image /= 255.0
        image = expand_dims(image, 0)
        return image, width, height

    def get_boxes(self, boxes, labels, thresh):
        """ Minden dobozra minden címkét letesztel, egy dobozra akár többet is """
    
        v_boxes, v_labels, v_scores = list(), list(), list()
        for box in boxes:
            for i in range(len(labels)):
                if box.classes[i] > thresh:
                    v_boxes.append(box)
                    v_labels.append(labels[i])
                    v_scores.append(box.classes[i]*100)

        return v_boxes, v_labels, v_scores

    def correct_yolo_boxes(self, boxes, image_h, image_w, net_h, net_w):  
        """ Itt átírtam az eredetit mert az nem ment """
        for i in range(len(boxes)):
            boxes[i].xmin = int(boxes[i].xmin * image_w)
            boxes[i].xmax = int(boxes[i].xmax * image_w)
            boxes[i].ymin = int(boxes[i].ymin * image_h)
            boxes[i].ymax = int(boxes[i].ymax * image_h)

    def detect(self, frame:VideoFrame, input_w = 256, input_h = 256, class_threshold = 0.6, labels = ["person"], anchors = [[116,90, 156,198, 373,326], [30,61, 62,45, 59,119], [10,13, 16,30, 33,23]]):
        """ 
            Bemeneti parméterek:
                input_w/h: modell bemeneti mérete
                class_treshold: ennyi konfidencia felett tartjuk meg a jelölt osztályokat
                labels: ezeket ismeri fel (be lehet rakni csomó mindent, fun)
                anchors: ezek alapján képzi le a BB-ket
    
            Feldolgozás lépései:
                1. Kép betöltése, előfeldolgozása
                2. Modell futtatása
                3. BoundigBox-ok előállítása 
                4. BB méret korrekció 
                5. átfedések kezelése
                4. BB címkézése
            
            Kimenet:
                boxes: befoglaló doboz
                labels: predikált osztály (nálunk ugye ez mindig person lesz, ezért kivehető akár)
                scores: ~konfidencia
        """
    
        image, image_w, image_h = self.load_image_pixels(frame,(input_w, input_h))
    
        yhat = self.model.predict(image)
        
        boxes = list()
        for i in range(len(yhat)):
            boxes += yolo.decode_netout(yhat[i][0], anchors[i], class_threshold, input_h, input_w)
        
        self.correct_yolo_boxes(boxes, image_h, image_w, input_h, input_w)
    
        yolo.do_nms(boxes, 0.5)
    
        boxes, labels, scores = self.get_boxes(boxes, labels, class_threshold)
    
        ret_boxes = []
        for box in boxes:
            y1, x1, y2, x2 = box.ymin, box.xmin, box.ymax, box.xmax
            width, height = x2 - x1, y2 - y1
            ret_boxes.append(BoundingBox(x1,y1,width,height))

        return ret_boxes, scores


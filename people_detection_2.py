import numpy as np
import time
import cv2
from video_frame import VideoFrame
from bounding_box import BoundingBox


class PeopleDetector:
    """
    People detection with YOLO.
    Attributes
    ----------
        model : keras model
            yolov2-tiny / yolov3-tiny / yolov3
    """

    def __init__(self, model = "yolov3-tiny"):
        self.net = cv2.dnn.readNetFromDarknet(model + ".cfg", model + ".weights")
        self.ln = self.net.getLayerNames()
        self.ln = [self.ln[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

    def detect(self, frame: VideoFrame, input_w=960, input_h=540, class_threshold=0.1):
        """
            Bemeneti parméterek:
                input_w/h: modell bemeneti mérete
                class_treshold: ennyi konfidencia felett tartjuk meg a jelölt osztályokat
                labels: ezeket ismeri fel (be lehet rakni csomó mindent, fun)

            Feldolgozás lépései:
                1. Kép betöltése, előfeldolgozása
                2. Modell futtatása, BoundigBox-ok előállítása
                3. átfedések kezelése

            Kimenet:
                boxes: befoglaló doboz
                scores: ~konfidencia
        """

        (H, W) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (input_w, input_h), swapRB=True, crop=False)
        self.net.setInput(blob)
        layerOutputs = self.net.forward(self.ln)

        boxes = []
        confidences = []

        for output in layerOutputs:
            for detection in output:
                scores = detection[5:]
                classID = np.argmax(scores)
                if classID == 0:
                    confidence = scores[classID]
                    if confidence > class_threshold:
                        box = detection[0:4] * np.array([W, H, H, W])
                        (centerX, centerY, width, height) = box.astype("int")
                        x = int(centerX - (width / 2))
                        y = int(centerY - (height / 2))
                        boxes.append([x, y, int(width), int(height)])
                        confidences.append(float(confidence))

        # apply non-maxima suppression to suppress weak, overlapping bounding boxes
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, class_threshold, 0.01)

        ret_boxes = []
        ret_confidences = []

        if len(idxs) > 0:
            for i in idxs.flatten():
                ret_boxes.append(BoundingBox(boxes[i][0], boxes[i][1], boxes[i][2], boxes[i][3]))
                ret_confidences.append(confidences[i])

        return ret_boxes, ret_confidences

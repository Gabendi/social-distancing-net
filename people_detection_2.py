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

    def __init__(self, model = "yolov3"):
        self.net = cv2.dnn.readNetFromDarknet(model + ".cfg", model + ".weights")
        self.ln = self.net.getLayerNames()
        self.ln = [self.ln[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

    def detect(self, frame: VideoFrame, input_w=960, input_h=540, class_threshold=0.1):
        """
            Detects people on the video frame.

            Detection process:
                1. Image pre-processing
                2. Predict and convert bounding boxes
                3. Non-maxima suppression

            Parameters
            ----------
                input_w : int
                    input image width
                input_h : int
                    input image height
                class_treshold : float
                    predictions below the given treshold are omitted

            

            Returns
            -------
                boxes: BoundingBox
                    predicted boundingboxes
                scores: float
                    prediction confindence
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

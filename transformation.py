import numpy as np
import cv2
from PIL import Image
from person import Coordinate

class Transformation:
    """
    Transforms camera coordinates to coordinates on the ground.

    Attributes
    ---------- 
        cameraCalibrationArray
            contains information about the orientation and placement of the camera
        frameWidth: int
            width of the videoFrame
        frameHeight: int
            heifht of the videoFrame
        
    """

    def __init__(self, cameraCallibrationArray, firstSectionToMeter, frameWidth, frameHeight)->None:
        self.cameraCallibrationArray = cameraCallibrationArray
        self.firstSectionToMeter = firstSectionToMeter
        self.frameWidth = frameWidth
        self.frameHeight = frameHeight

        self.four_point_transform();


    def order_points(self, pts):
        rect = np.zeros((4, 2), dtype = "float32")

        s = pts.sum(axis = 1)
        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]

        diff = np.diff(pts, axis = 1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]

        return rect

    def four_point_transform(self):
        rect = self.cameraCallibrationArray
        (tl, tr, br, bl) = rect

        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))

        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))
        
        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype = "float32")

        print(dst)

        M = cv2.getPerspectiveTransform(rect, dst)
        print(np.dot(M, [[0],[0],[1]])[0][0])
        print(np.dot(M, [[0],[0],[1]])[1][0])
        trans = np.array([
            [1, 0, -np.dot(M, [[0],[0],[1]])[0][0]],
            [0, 1, -np.dot(M, [[0],[0],[1]])[1][0]],
            [0, 0, 1]], dtype = "float32")
        
        transformed = np.dot(trans, M)
     
        self.transformedFrameWidth = np.dot(transformed, [[self.frameWidth],[0],[1]])[0][0] / np.dot(transformed, [[self.frameWidth],[0],[1]])[2][0]
        self.transformedFrameHeight = np.dot(transformed, [[0],[self.frameHeight],[1]])[1][0] / np.dot(transformed, [[0],[self.frameHeight],[1]])[2][0]


        self.transformationMatrix = transformed;
        self.inverseTransformationMatrix = np.dot(np.linalg.pinv(M), np.linalg.pinv(trans))

    def transformPoint(self, x, y):
        p = np.dot(self.transformationMatrix, [[x], [y], [1]])
        p = p / p[2]
        return p[0], p[1]

    def getTransformedPixelNumberOfMeter(self):
        (tl, tr, br, bl) = self.cameraCallibrationArray

        d = Coordinate(tl[0], tl[1]).DistanceFrom(Coordinate(tr[0], tr[1]))
        
        ttl = self.transformPoint(tl[0], tl[1])
        ttr = self.transformPoint(tr[0], tr[1])


        td = Coordinate(ttl[0], ttl[1]).DistanceFrom(Coordinate(ttr[0], ttr[1]))

        return td * self.firstSectionToMeter
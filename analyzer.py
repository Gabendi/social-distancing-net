from person import Person
from typing import List
from violation import Violation
from video_frame import VideoFrame

from tracker import Tracker

from people_detection_2 import PeopleDetector
from CalculateDistanceViolations import CalculateDistanceViolations

class Analyzer:
    """
    Analyzes the CCTV footage.

    Attributes
    ---------- 
        video : VideoFrame[]
            videoframes of the video
            
        violations : Violation[]
            violations happened on footage
        activePeople: Person[]
            people currently on video
    """
    def __init__(self, transformation, model)->None:
        self.transformation = transformation

        self.video:List[VideoFrame]=[]
        self.violations:List[Violation]=[]
        self.activePeople:List[Person]=[]
        self._tracker=Tracker(self,transformation.getTransformedPixelNumberOfMeter() * 1.8)
        self._peopledetector=PeopleDetector(model = model)

        #Callibration calculations
        print("1.8 meter:")
        print(transformation.getTransformedPixelNumberOfMeter() * 1.8)
        self.calculateDistanceViolations = CalculateDistanceViolations(transformation.getTransformedPixelNumberOfMeter() * 1.8)


        
    
    def add_video_frame(self, video_frame:VideoFrame)->None:
        """Recieves and analizes the new vide frame.
        Updates, the violations array with the new violations found

        Parameters
        ----------
            video_frame : VideoFrame
                New VideFrame
        """
        self.video.append(video_frame)
        
        boundingboxes, scores=self._peopledetector.detect(video_frame)

        self._tracker.updateTrajectories(video_frame, boundingboxes, scores)
        
        self._tracker.groupTrajectories()

        self.violations = self.calculateDistanceViolations.CalculateViolations(self.activePeople)

    def calibrate(self, video_frame : VideoFrame):
        raise NotImplementedError()
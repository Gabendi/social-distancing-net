from person import Person
from typing import List
from violation import Violation
from video_frame import VideoFrame

from tracker import Tracker

from people_detection import PeopleDetector
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
    def __init__(self, transformation)->None:
        self.video:List[VideoFrame]=[]
        self.violations:List[Violation]=[]
        self.activePeople:List[Person]=[]
        self._tracker=Tracker(self)
        self._peopledetector=PeopleDetector()

        #Callibration calculations
        self.transformation = transformation
        self.calculateDistanceViolations = CalculateDistanceViolations(transformation.transformedFrameWidth * 1.8)


        
    
    def add_video_frame(self, video_frame:VideoFrame)->None:
        """Recieves and analizes the new vide frame.
        Updates, the violations array with the new violations found

        Parameters
        ----------
            video_frame : VideoFrame
                New VideFrame
        """
        last_video_frame=self.video[len(self.video)-1] if len(self.video)>0 else None
        self.video.append(video_frame)
        
        boundingboxes, scores=self._peopledetector.detect(video_frame)

        self._tracker.updateTrajectories(video_frame,last_video_frame,boundingboxes,scores)
        self._tracker.groupTrajectories()

        self.violations = self.calculateDistanceViolations.CalculateViolations(self.activePeople)

    def calibrate(self,video_frame:VideoFrame):
        raise NotImplementedError()
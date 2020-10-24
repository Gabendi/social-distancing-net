from typing import List
from violation import Violation
from video_frame import VideoFrame

from tracker import Tracker

class Analyzer:
    """
    Analyzes the CCTV footage.

    Attributes
    ---------- 
        video : VideoFrame[]
            videoframes of the video
            
        violations : Violation[]
            violations happened on footage
    """
    def __init__(self)->None:
        self.video=List[VideoFrame]
        self.violations=List[Violation]
        self._tracker=Tracker()
        
    
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
        
        self._tracker.updateTrajectories(video_frame,last_video_frame)
        #TODO call CalculateDistanceViolations
        raise NotImplementedError()

    def calibrate(self,video_frame:VideoFrame):
        raise NotImplementedError()
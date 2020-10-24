from video_frame import VideoFrame
from people_detection import PeopleDetector

class Tracker:
    """
    Identifies and stores detected people, identifies groups.

    Attributes
    ---------- 
        activePeople : Person[]
            list of people currently in the view of the camera
    """
    def __init__(self) -> None:
        self._peopledetector=PeopleDetector()
        self.activePeople=[]

    def updateTrajectories(self,current:VideoFrame,last:VideoFrame=None)->None:
        """
        Identifies new people on the videoFrame, tracks already identified people. Update groups
        Parameters
        ----------
            current : VideoFrame
                New video frame
            last : VideoFrame, optional
                The video frame before, by default None

        """
        current_bounding_boxes=self._peopledetector.detect(current)
        
        raise NotImplementedError()

    def groupTrajectories()->None:
        """
        Updates groups
        """
        raise NotImplementedError()

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

    def groupTrajectories(self, d = 2, dt = 4 * 30)->None:
        """
        Considers two individuals as being in the same group if they are less then d meters apart for at least dt seconds.
        Parameters
        ----------
            d : int
                distance
            dt : int
                min seconds (sec * fps)
        """
        for i, p1 in enumerate(self.activePeople):
            for j, p2 in enumerate(self.activePeople):
                if (i > j) and (p1 not in p2.inGroupWith):
                    t = 0
                    max_t = 0
                    for k in range(len(p1.coordinates)):
                        if (p1.coordinates[k].DistanceFrom(p2.coordinates[k]) <= d):
                            t += 1
                            if t > max_t:
                                max_t = t
                        else:
                            t = 0
                    if max_t >= dt:
                        p1.inGroupWith.append(p2)
                        p2.inGroupWith.append(p1)


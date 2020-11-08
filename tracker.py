from person import Person
from bounding_box import BoundingBox
from typing import List
from video_frame import VideoFrame
from sort import Sort
import numpy as np

class Tracker:
    """
    Identifies and stores detected people, identifies groups.

    Attributes
    ---------- 
        activePeople : Person[]
            list of people currently in the view of the camera
    """
    def __init__(self, analyzer) -> None:
        self._sort=Sort()
        self._analyzer=analyzer
        pass
    
    def addBoundingBoxForPerson(self, person:Person, box:BoundingBox):
        person.bounding_boxes.append(box)
        x, y = self._analyzer.transformation.transformPoint(box.left+box.width/2, box.top+box.height)
        person.addCoordinates(x, y)

    def updateTrajectories(self,current:VideoFrame,last:VideoFrame,bounding_boxes:List[BoundingBox],scores:List[float])->None:
        """
        Identifies new people on the videoFrame, tracks already identified people. Update groups
        Parameters
        ----------
            current : VideoFrame
                New video frame
            last : VideoFrame, optional
                The video frame before, by default None
            bounding_boxes: BoundingBox[]
                Detected boundingboxes on current frame
            scores: float[]
                Certanity score of boundingboxes
        """
        lenBB=len(bounding_boxes);
        bbs=np.zeros((lenBB,5))
        npbb=np.array([[bb.left, bb.top, bb.left+bb.width,bb.top+bb.height] for bb in bounding_boxes])
        npscores=np.array(scores)
        npscores=np.resize(npscores,(lenBB,1))
        bbs=np.hstack((npbb,npscores))
        objs=self._sort.update(bbs)
        activePeople:List[Person]=self._analyzer.activePeople
        to_delete=[]
        for person in activePeople:
            found=False
            for obj in objs:
                if obj[4]==person.id:
                    self.addBoundingBoxForPerson(person, BoundingBox(int(obj[0]),int(obj[1]),int(obj[2]-obj[0]),int(obj[3]-obj[1])))
                    found=True
                    obj[4]=-1
                    break
            if not found:
                countNone=0
                for bbid in range(1,min(len(person.bounding_boxes),6)):
                    if person.bounding_boxes[-bbid] is None:
                        countNone+=1
                if(countNone==5):
                    to_delete.append(person)
                person.bounding_boxes.append(None)
        for obj in objs:
            if obj[4]!=-1:
                newPerson=Person()
                newPerson.id=obj[4]
                self.addBoundingBoxForPerson(newPerson, BoundingBox(int(obj[0]),int(obj[1]),int(obj[2]-obj[0]),int(obj[3]-obj[1])))
                self._analyzer.activePeople.append(newPerson)   
        for d in to_delete:
            self._analyzer.activePeople.remove(d)

        

    def groupTrajectories(self, d = 2, dt = 4 * 30)->None:
        """
        Considers two individuals as being in the same group if they are less then d meters apart for at least dt seconds.
        Parameters
        ----------
            d : int
                maximum distance
            dt : int
                minimum seconds (sec * fps)
        """
        for i, p1 in enumerate(self._analyzer.activePeople):
            for j, p2 in enumerate(self._analyzer.activePeople):
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


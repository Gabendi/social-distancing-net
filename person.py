from typing import List
from bounding_box import BoundingBox
import math

class Coordinate:
    """
        Transformed x-y coordinates.
    """
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
    def DistanceFrom(self, other):
        return math.sqrt( (self.x - other.x)**2 + (self.y - other.y)**2 )      

class Person:
    """
    A detected person

    Attributes
    ---------- 
        id : int
            id of a Person
        bounding_boxes : BoundingBox[]
            bounding boxes of the same person.
            Every item is a BoundingBox or None if a boundingbox is missing
        coordinates : Coordinate[]
            coordinates of the person, None if missing
        inGroupWith : Person[]
            If a person walks together with others, they are a group or family.
    """
    maxid=0
    def __init__(self)->None:
        self.id=self._getNewID()
        self.bounding_boxes: List[BoundingBox]=[]
        self.inGroupWith :List[Person]=[] 
        self.coordinates :List[Coordinate]=[] 

    @classmethod
    def _getNewID(cls)->int:
        newid=cls.maxid
        cls.maxid+=1
        return newid

    def addBoundingBox(self, x = None, y = None) -> None:
        """
            Add the next (t.) transformed x-y coordinates, or None if it is missing at time t.
            TODO: ezt majd Jonatánnak kéne hívni
                Egyenlőre időt nem tárol, amelyik időpillanban nincs adat ott None van
        """
        if x != None :
            self.coordinates.append(Coordinate(x,y))
        else:
            self.coordinates.append(None)
    
    def addCoordinates(self, x = None, y = None) -> None:
        """
            Add the next (t.) transformed x-y coordinates, or None if it is missing at time t.
            TODO: ezt majd Jonatánnak kéne hívni
                Egyenlőre időt nem tárol, amelyik időpillanban nincs adat ott None van
        """
        if x != None :
            self.coordinates.append(Coordinate(x,y))
        else:
            self.coordinates.append(None)

    def getCenter(self):
        box = self.bounding_boxes[len(self.bounding_boxes) - 1]
        if(box == None):
            return;
        return (box.left + box.width/2, box.top + box.height / 2)

    def getCoordinate(self):
        return self.coordinates[len(self.coordinates) -1 ]

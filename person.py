from typing import List, Tuple, Union
from bounding_box import BoundingBox
import math

class Coordinate:
    """
        Coordinates of a point a 2D plane

        Attributes
        ----------
            x: int
                x coordinate of the point
            y: int
                y coordinate of the point
    """
    def __init__(self,x:int,y:int):
        self.x = x
        self.y = y
        
    def DistanceFrom(self, other)->float:
        """
        Calculates the distance between this point and another point

        Parameters
        ----------
            other : Coordinate
                other point

        Returns
        -------
            float
                Distance between the points
        """
        return math.sqrt( (self.x - other.x)**2 + (self.y - other.y)**2 )      

class Person:
    """
    A detected person.
    Contains the bounding_boxes of the person from his/her first detection until the person disapears for at least 15 video frame.
    
    It also contains the coordinates of the person. They are 2D coordinates the predefined ground plane.
    
    If a person walks together with others, they are a group or family. Each person stores their fellow group or family members.

    Attributes
    ---------- 
        id : int
            id of a Person
        bounding_boxes : BoundingBox[]
            bounding boxes of the same person.
            Every item is a BoundingBox or None if a boundingbox is missing
        coordinates : Coordinate[]
            Bottom middle coordinates the boundingboxes of the person, None if missing
        inGroupWith : Person[]
            Others in the same group with the person
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
    
    def addCoordinates(self, x:int = None, y:int = None) -> None:
        """
        Add the next (t.) transformed x-y coordinates, or None if it is missing at time t.
        """
        if x != None :
            self.coordinates.append(Coordinate(x,y))
        else:
            self.coordinates.append(None)

    def getCenter(self)->Union[Tuple[float],None]:
        """
        Returns the center of the boundingbox of the person in the last video frame, or None if the last boundingbox is missing

        Returns
        -------
            Union[Tuple[float],None]
                x-y coordinates of the center of the boundingbox or None if missing
        """
        box = self.bounding_boxes[len(self.bounding_boxes) - 1]
        if(box == None):
            return;
        return (box.left + box.width/2, box.top + box.height / 2)

    def getCoordinate(self)->Coordinate:
        """
        Returns the coordinate of the person in the last video frame or None if missing
        Returns
        -------
            Coordinate
                Coordinate of the person or None if missing
        """
        return self.coordinates[len(self.coordinates) -1 ]

from bounding_box import BoundingBox

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
        inGroupWith : Person[]
            If a person walks together with others, they are a group or family.
    """
    maxid=0
    def __init__(self):
        self.id=self._getNewID()
        self.bounding_boxes=[]
        self.inGroupWith=[]

    @classmethod
    def _getNewID(cls)->int:
        newid=maxid
        maxid+=1
        return newid


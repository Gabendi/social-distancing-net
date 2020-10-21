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
        self.id=self.getNewID()
        self.bounding_boxes=[]
        self.inGroupWith=[]

    @classmethod
    def getNewID(cls)->int:
        """Generates a new unique id for a person

        Returns
        -------
            int
                new unique id
        """
        newid=maxid
        maxid+=1
        return newid


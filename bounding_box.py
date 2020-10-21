class BoundingBox:
    """
    BoundingBox of a Person

    Attributes
    ---------- 
        left : int
            left of the boundingbox in pixels
        top : int
            top of the boundingbox in pixels
        width : int
            width of the boundingbox in pixels
        height : int
            height of the boundingbox in pixels
    """
    def __init__(self,left:int,top:int,width:int,height:int):
        """
        Parameters
        ----------
            left : int
                left of the boundingbox in pixels
            top : int
                top of the boundingbox in pixels
            width : int
                width of the boundingbox in pixels
            height : int
                height of the boundingbox in pixels
        """
        self.top=top
        self.left=left
        self.width=width
        self.height=height
        
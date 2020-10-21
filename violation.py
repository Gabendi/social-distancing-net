class Violation:
    """
    A violation of social distancing

    Attributes
    ---------- 
        x : int
            x coordinate of a violation
        y : int
            y coordinate of a violation
        time : int
            time of the violation in unix timestamp
    """

    def __init__(self,x:int,y:int,time:int):
        """
        Parameters
        ----------
            x : int
                x coordinate of a violation
            y : int
                y coordinate of a violation
            time : int
                time of the violation in unix timestamp
        """
        self.x=x
        self.y=y
        self.time=time
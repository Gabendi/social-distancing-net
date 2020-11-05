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
        accepted: boolean
            true if this is an accepted violation between group members
    """

    def __init__(self,x:int,y:int,time:int, accepted:booelan = False)->None:
        """
        Parameters
        ----------
            x : int
                x coordinate of a violation
            y : int
                y coordinate of a violation
            time : int
                time of the violation in unix timestamp
            accepted: boolean
                true if this is an accepted violation between group members
        """
        self.x=x
        self.y=y
        self.time=time
        self.accepted = accepted
from person import Person

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

    def __init__(self,p1:Person,p2:Person,time:int, accepted:bool = False)->None:
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
        self.p1=p1
        self.p2=p2
        self.time=time
        self.accepted = accepted
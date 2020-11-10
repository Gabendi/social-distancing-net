
from person import Person
from violation import Violation  
class CalculateDistanceViolations:
    """
        This class calculates the violations in each frame.

        Attributes
        ----------
            t : int
                Current time.
                Measured as a number of frames since the beginning of the video.
            minDist: int
                Minimum distance (m).
                Violation is created if somebody violates to keep this minimum distance.
    """

    def __init__(self, minDist = 2):
        self.t = 0
        self.minDist = minDist

    def CalculateViolations(self, activePeople):
        """
        Calculates the last violations.

        Parameters
        ----------
            activePeople : Person[]
                Active people in the last videoframe
        """
        returnViolations = []
        for i, p1 in enumerate(activePeople):
            for j, p2 in enumerate(activePeople):
                if (i > j and p1.getCoordinate()!=None and p2.getCoordinate()!=None and p1.getCoordinate().DistanceFrom(p2.getCoordinate()) < self.minDist):
                    returnViolations.append(Violation(p1, p2, self.t, p1 in p2.inGroupWith))

        self.t += 1
        return returnViolations



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

    def CalculateViolations(self, activePeople :List[Person]) -> list[Violation]:
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
                if (i > j):
                    if (p1.Coordinate.DistanceFrom(p2.Coordinate) < self.minDist):
                        if p1 not in p2.inGroupWith:
                            returnViolations.append(Violation(p1.Coordinate.x, p1.Coordinate.y, self.t))
                            returnViolations.append(Violation(p2.Coordinate.x, p2.Coordinate.y, self.t))
                        else:
                            returnViolations.append(Violation(p1.Coordinate.x, p1.Coordinate.y, self.t, True))
                            returnViolations.append(Violation(p2.Coordinate.x, p2.Coordinate.y, self.t, True))

        self.t += 1
        return returnViolations

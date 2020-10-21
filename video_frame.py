import numpy
class VideoFrame:
    """
    A frame of the recorded video.

    Attributes
    ---------- 
        n : static int
            width of a frame
        m : static int
            height of a frame
        pixels : n x m x 3 numpy array
            numpy array containing pixel values (dtype: int8)
    """
    n=1280
    m=720
    def __init__(self,pixels):
        """

        Parameters
        ----------
            pixels : n x m x 3 numpy array
                numpy array containing pixel values (dtype: int8)
        """
        self.pixels=pixels
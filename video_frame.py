from typing import List
import numpy
class VideoFrame:
    """
    A frame of the recorded video.

    Attributes
    ---------- 
        width : static int
            width of a frame
        heigh t: static int
            height of a frame
        pixels : width x height x 3 numpy array
            numpy array containing pixel values (dtype: int8)
    """
    width=1280
    height=720
    def __init__(self,pixels)->None:
        """

        Parameters
        ----------
            pixels : width x height x 3 numpy array
                numpy array containing pixel values (dtype: int8)
        """
        self.pixels=pixels
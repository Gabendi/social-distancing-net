import numpy
class VideoFrame:
    """
    A frame of the recorded video.

    Attributes
    ---------- 
        pixels : n x m x 3 numpy array
            numpy array containing pixel values (dtype: int8)
    """
    def __init__(self,pixels):
        """[summary]

        Parameters
        ----------
            pixels : n x m x 3 numpy array
                numpy array containing pixel values (dtype: int8)
        """
        self.pixels=pixels
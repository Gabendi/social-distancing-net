from video_frame import VideoFrame

class Analyzer:
    """
    Analyzes the CCTV footage.

    Attributes
    ---------- 
        video : VideoFrame[]
            videoframes of the video
            
        violations : Violation[]
            violations happened on footage
    """
    def __init__(self):
        self.video=[]
        self.violations=[]
    
    def AddVideoFrame(self, video_frame:VideoFrame):
        """Recieves and analizes the new vide frame.
        Updates, the violations array with the new violations found

        Parameters
        ----------
            video_frame : VideoFrame
                New VideFrame
        """
        self.video.append(video_frame)
        #TODO call object detection
        #TODO call CalculateDistanceViolations
        raise NotImplementedError()

    def Calibrate(self,video_frame:VideoFrame):
        raise NotImplementedError()
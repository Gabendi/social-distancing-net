from yolo3_one_file_to_detect_them_all import bbox_iou
from analyzer import Analyzer
import cv2
import sys
from tensorflow.keras.models import load_model
from numpy import expand_dims
from matplotlib import pyplot
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import numpy as np
from transformation import Transformation
import time


from people_detection import PeopleDetector



def help()->None:
    """
        Displays help message in console
    """
    print('\n')
    print('This script is for visualizing bounding-box estimations for detection of human bodies.')
    print('Usage: python reading_script.py [VideoStream]')
    print('\n')


def runStream(videoUrl, model, sample_rate=0.1):
    """
    Processes the prerecorded video, or webcam, and displays the analyzed video.
    The program processes only a few selected videoframes for performance reasons.
    Sample rate specifies what portion of the video is processed.
    A video frame if processed if video_frame_index mod 1/sample_rate is 0.

    At the end of the processing the program displays the density of the violations on a heatmap.

    Parameters
    ----------
        videoUrl
            Path of the prerecorded video file, if None the program processes the  webcam stream
        model
            YOLO type, must be yolov3, yolov3-tiny or yolov2-tiny
        sample_rate : float, optional
            Sample rate of processing, by default 0.1
    """
    vc = cv2.VideoCapture(videoUrl)

    frameWidth = 1920 // 2
    frameHeight = 1080 // 2
    
    cameraCallibrationArray = np.array([(387,231),(683,279),(515,462),(154,373)], dtype = "float32")
    firstSectionToMeter = 0.21
    transformation = Transformation(cameraCallibrationArray, firstSectionToMeter, frameWidth, frameHeight)
    analyzer=Analyzer(transformation, model = model)

    print(videoUrl)
    last_time=time.perf_counter()
    counter=0
    s=int(1/sample_rate)

    heatMap = np.zeros((frameWidth, frameHeight))

    while True:
        ret, frame = vc.read()
     #   img, width, height = peopleDetector.load_image_pixels(frame, frame.shape)
        if counter%s!=0: # process every s th frame
            counter+=1
            continue
        if ret==False:
            break
        
        print(frame.shape) 
        
        frame = cv2.resize(frame, (frameWidth, frameHeight))  
        analyzer.add_video_frame(frame) 

        #(x,y,width,height) tuple
        #boxes, labels, scores = Detect(frame)
        for person in analyzer.activePeople:
            bbox=person.bounding_boxes[-1]
            if not(bbox is None):
                x,y,w,h = bbox.left, bbox.top, bbox.width, bbox.height
                frame=cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 1)
                frame=cv2.putText(frame, f"Person {person.id}", (x+w+10, y+h), 0, 0.3, (0,255,0))
                # add bbox center to heatmap
                for i in range(-5, 5):
                    for j in range(-5, 5):
                        if x + i > 0 and y + j > 0:
                            heatMap[x + i][y + j] += 1

        for violation in analyzer.violations:
            color = (255, 0, 0)
            if violation.accepted:
                color = (255, 255, 0)
            #print(violation.p1.getCoordinate().x)
            #print(violation.p1.getCoordinate().y)
            if(violation.p1.getCenter() == None or violation.p2.getCenter() == None):
                continue
            from_p = (int(violation.p1.getCenter()[0]), int(violation.p1.getCenter()[1]))
            to_p = (int(violation.p2.getCenter()[0]), int(violation.p2.getCenter()[1]))
            cv2.line(frame, from_p, to_p, color, 2)

            #Map view
            #cv2.rectangle(frame, (0,0), (frameWidth/5,frameHeight/5), (0,0,0), -1)
            #from_p = (int(violation.p1.getCoordinate().x/10), int(violation.p1.getCoordinate().y/10))
            #to_p = (int(violation.p2.getCoordinate().x/10), int(violation.p2.getCoordinate().y/10))
            #cv2.line(frame, from_p, to_p, color, 2)
		
        transformed = transformation.transformationMatrix
        width = transformation.transformedFrameWidth
        height = transformation.transformedFrameHeight
        warped = cv2.warpPerspective(frame, transformed, (int(width), int(height)))
        warped = cv2.resize(warped, (int(width/2), int(height/2)))  
        cv2.imshow('Human detection example', frame)
        current_time=time.perf_counter()
        #print(f"{(s)/(current_time-last_time):0.4f} fps")
        last_time=current_time
        counter+=1
		
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    #Display created heatmap
    plt.imshow(heatMap, cmap='hot', interpolation='nearest')
    plt.show()
	
    #Release resources
    vc.release()
    cv2.destroyAllWindows()
	
if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print('\nToo few arguments, see usage:')
        help()
    else:
        VIDEO_STREAM = sys.argv[1]
        model = 'yolov3'
        if (len(sys.argv) > 2):
            if sys.argv[2] == "yolov2-tiny" or sys.argv[2] == "yolov3-tiny" or sys.argv[2] == "yolov3":
                model = sys.argv[2]
            else:
                print('\nProblem with the model argument, the default will be yolov3')
                print('\nNext time try "yolov3" or "yolov3-tiny" or "yolov2-tiny"')
        runStream(VIDEO_STREAM, model)

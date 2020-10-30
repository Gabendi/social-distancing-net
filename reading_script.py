from yolo3_one_file_to_detect_them_all import bbox_iou
from analyzer import Analyzer
import cv2
import sys
from tensorflow.keras.models import load_model
from numpy import expand_dims
from matplotlib import pyplot
from matplotlib.patches import Rectangle


from people_detection import PeopleDetector

#importing our code to do the prediction

def help():
	print('\n')
	print('This script is for visualizing bounding-box estimations for detection of human bodies.')
	print('Usage: python reading_script.py [VideoStream]')
	print('\n')


def runStream(videoUrl):
    vc = cv2.VideoCapture(videoUrl)
    analyzer=Analyzer()
	
    print(videoUrl)
    while True:
        ret, frame = vc.read()
     #   img, width, height = peopleDetector.load_image_pixels(frame, frame.shape)
        print(frame.shape) 
        frame = cv2.resize(frame, (1920//4, 1080//4))  
        analyzer.add_video_frame(frame)
        print(f"activePeople {len(analyzer.activePeople)}")
        #(x,y,width,height) tuple
        #boxes, labels, scores = Detect(frame)
        for person in analyzer.activePeople:
            bbox=person.bounding_boxes[-1]
            if not(bbox is None):
                x,y,w,h = bbox.left, bbox.top, bbox.width, bbox.height
                frame=cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 1)
                frame=cv2.putText(frame, f"Person {person.id}", (x+w+10, y+h), 0, 0.3, (0,255,0))
		
        cv2.imshow('Human detection example', frame)
		
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
		
    vc.release()
    cv2.destroyAllWindows()
	
if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print('\nToo few arguments, see usage:')
        help()
    else:
        VIDEO_STREAM = sys.argv[1]
        runStream(VIDEO_STREAM)

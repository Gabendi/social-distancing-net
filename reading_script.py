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
    peopleDetector = PeopleDetector()
	
    print(videoUrl)
    while True:
        ret, frame = vc.read()
     #   img, width, height = peopleDetector.load_image_pixels(frame, frame.shape)
        print(frame.shape) 
        #frame = cv2.resize(frame, (1920//4, 1080//4))  
        bboxes = peopleDetector.detect(frame)
       
        #(x,y,width,height) tuple
        #boxes, labels, scores = Detect(frame)
		
        for bbox in bboxes:
            x,y,w,h = bbox.top, bbox.left, bbox.width, bbox.height
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
            cv2.putText(frame, 'Person', (x+w+10, y+h), 0, 0.3, (0,255,0))
		
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

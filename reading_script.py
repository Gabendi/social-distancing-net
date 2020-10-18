import cv2
import sys

def help():
	print('\n')
	print('This script is for visualizing bounding-box estimations for detection of human bodies.')
	print('Usage: python reading_script.py [VideoStream]')
	print('\n')

def makePrediction(frame):
	raise NotImplementedError()

def runStream(videoUrl):
	videoCapture = cv2.VideoCapture(videoUrl)
	
	while True:
		ret, frame = videoCapture.read()		
		
		#(x,y,width,height) tuple
		bboxArray = makePrediction(frame)
		
		for bbox in bboxArray:
			x,y,w,h = bbox
			cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
			cv2.putText(im, 'Person', (x+w+10, y+h), 0, 0.3, (0,255,0))
		
		cv2.imshow('Human detection example', frame)
		
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		
	cap.release()
	cv2.destroyAllWindows()
	
if __name__ == "__main__":
	if(len(sys.argv) < 2):
		print('\nToo few arguments, see usage:')
		help()
	else:
		VIDEO_STREAM = sys.argv[1]
		runStream(VIDEO_STREAM)
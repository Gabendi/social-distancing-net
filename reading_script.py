import cv2
import sys
from tensorflow.keras.models import load_model
from numpy import expand_dims
from matplotlib import pyplot
from matplotlib.patches import Rectangle

#importing our code to do the prediction
import yolo3_one_file_to_detect_them_all as yolo

def help():
	print('\n')
	print('This script is for visualizing bounding-box estimations for detection of human bodies.')
	print('Usage: python reading_script.py [VideoStream]')
	print('\n')


def preprocess_image(image, shape = (416, 416)):
    image /= 255.0
    image = expand_dims(image, 0)
    return image, width, height

def get_boxes(boxes, labels, thresh):
    """ Minden dobozra minden címkét letesztel, egy dobozra akár többet is """
    
    v_boxes, v_labels, v_scores = list(), list(), list()
    for box in boxes:
        for i in range(len(labels)):
            if box.classes[i] > thresh:
                v_boxes.append(box)
                v_labels.append(labels[i])
                v_scores.append(box.classes[i]*100)

    return v_boxes, v_labels, v_scores

def draw_boxes(filename, v_boxes, v_labels, v_scores):
    """ képre kirajzolja a dobozokat, kiírja az osztályt és a pontot is"""
    
    data = pyplot.imread(filename)
    pyplot.imshow(data)

    ax = pyplot.gca()
    for i in range(len(v_boxes)):
        box = v_boxes[i]

        y1, x1, y2, x2 = box.ymin, box.xmin, box.ymax, box.xmax
        width, height = x2 - x1, y2 - y1
        rect = Rectangle((x1, y1), width, height, fill=False, color='white')

        ax.add_patch(rect)
        label = "%s (%.3f)" % (v_labels[i], v_scores[i])
        pyplot.text(x1, y1, label, color='white')

    pyplot.show()

def Detect(image, input_w = 416, input_h = 416, class_threshold = 0.6, labels = ["person"], anchors = [[116,90, 156,198, 373,326], [30,61, 62,45, 59,119], [10,13, 16,30, 33,23]]):
    """ 
        Bemeneti parméterek:
            input_w/h: modell elvárt bemeneti mérete
            class_treshold: ennyi konfidencia felett tartjuk meg a jelölt osztályokat
            labels: ezeket ismeri fel (be lehet rakni csomó mindent, fun)
            anchors: valahogy ezek alapján képzi le a BB-ket
                     nem tudom az anchort hogy kell módosítani, azt hittem a YOLO pont azt tudja, hogy ezzel nem kell szívni már
    
        Feldolgozás lépései:
            1. Kép betöltése, előfeldolgozása
            2. Modell futtatása
            3. BoundigBox-ok előállítása 
            4. BB méret korrekció 
            5. átfedések kezelése
            4. BB címkézése
            
        Kimenet:
            boxes: befoglaló doboz
            labels: predikált osztály (nálunk ugye ez mindig person lesz, ezért kivehető akár)
            scores: ~konfidencia
    """
    image_w = image.shape[1]
    image_h = image.shape[0]
    #image, image_w, image_h = load_image_pixels(photo_filename,(input_w, input_h))
    #TODO ide kéne varázsolni a modellt
    yhat = model.predict(image)
        
    boxes = list()
    for i in range(len(yhat)):
        boxes += yolo.decode_netout(yhat[i][0], anchors[i], class_threshold, input_h, input_w)
        
    yolo.correct_yolo_boxes(boxes, image_h, image_w, input_h, input_w)
    
    yolo.do_nms(boxes, 0.5)
    
    boxes, labels, scores = get_boxes(boxes, labels, class_threshold)
    
    return boxes, labels, scores

def runStream(videoUrl):
	vc = cv2.VideoCapture(videoUrl)
	
	
	print(videoUrl)
	while True:
		ret, frame = vc.read()		
		
		#(x,y,width,height) tuple
		boxes, labels, scores = Detect(frame)
		
		# for bbox in bboxArray:
			# x,y,w,h = bbox
			# cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
			# cv2.putText(im, 'Person', (x+w+10, y+h), 0, 0.3, (0,255,0))
		
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
		model = load_model('model.h5')
		VIDEO_STREAM = sys.argv[1]
		runStream(VIDEO_STREAM)

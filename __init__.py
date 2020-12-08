"""
# SocialDistancingNet
This program helps the fight against recent pandemic caused by the corona virus.
To prevent the spread of the virus its important that all of us follow the social distancing guidelines proposed by the World Health Organization.
This program is capable of identifying violations of social distancing using a CCTV camera footage and helps the shop owners for better design better shop layouts and goverments to place space dividers in public areas.

## Installation

First you need install the required packages using the requirements.txt:

```console
$pip3 install -r requirements.txt
```

Then download a pretrained yolo network from the [offical website](https://pjreddie.com/darknet/yolo/). Use Tiny YOLO for faster or YOLOv3-416 for more precise processing.
The cfg and weights files must be placed in the root folder of the project.

## Usage:
```console
$python3 reading_script.py [VideoStream] [Model]
```

### [VideoStream]
It can be either path of a prerecorded video or '0' for webcamera live stream.

### [Model]
Select wich [yolo](https://pjreddie.com/darknet/yolo/) model to use, options:
    - '"yolov3"' : High accuracy, but real-time processing is resource intensive
    - '"yolov3-tiny"/"yolov2-tiny"': Lower accuracy but near real-time processing on medium hardware resources  
The program looks for the corresponding cfg and weights files.

### camera_conf.json
Contains information for camera calibration. It contains the pixel coordinates of a square on the ground
  - `factorToMeter`: side length of the square in meters
 -  `cameraCallibrationArray`: pixel coordinates of the square
```
 
## Examples

The program displays the detected violations:
    - Each detected person is surrounded with its boundingbox
    - The unique identifier of the detected person is displayed below the boundingbox
    - Dark blue lines display social distancing violations between strangers
    - Light blue lines display social distancing violations within groups/families (this violations can be ignored)

<iframe src="https://drive.google.com/file/d/1bdB-Zhx3nq0vSdlsCWC0RMQldPuAjkZu/preview" width="640" height="480"></iframe>

Detected couples:

<iframe src="https://drive.google.com/file/d/1JNctJjKfSG-HG5TSBf9xF5weJqsInRPC/preview" width="640" height="480"></iframe>

<iframe src="https://drive.google.com/file/d/10W9QQJU9xkHoEGYKQxckc1ztrwGlbbSr/preview" width="640" height="480"></iframe>

Social distancing violation between couples:

<iframe src="https://drive.google.com/file/d/1aGQP5NmE9j6EBwgTQHzKJ1qVDsri7SjI/preview" width="640" height="480"></iframe>

Multiple detected social distancing violations:

<iframe src="https://drive.google.com/file/d/1Tu3S2gFRvraJlJzy4dhnWi52farmCDUs/preview" width="640" height="480"></iframe>
"""
__pdoc__ = {}
__pdoc__['venv'] = False
__pdoc__['yolo3_one_file_to_detect_them_all'] = False
__pdoc__['people_detection'] = False
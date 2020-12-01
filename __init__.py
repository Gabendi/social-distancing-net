"""
# SocialDistancingNet
This program helps the fight against recent pandemic caused by the corona virus.
To prevent the spread of the virus its important that all of us follow the social distancing guidelines proposed by the World Health Organization.
This program is capable of identifying violations of social distancing using a CCTV camera footage and helps the shop owners for better design better shop layouts and goverments to place space dividers in public areas.

## Installation

First you need install the required packages using the requirements.txt:

```$pip3 install -r requirements.txt```

Then download a pretrained yolo network from the [offical website](https://pjreddie.com/darknet/yolo/). Use Tiny YOLO for faster or YOLOv3-416 for more precise processing.
The cfg and weights files must be placed in the root folder of the project.

## Usage:

Either analyze a prerecorded video:

```$python3 reading_script.py /path/to/video```

Or analyze live webcamera stream:

```$python3 reading_script.py 0 yolov3/yolov3-tiny/yolov2-tiny asd.json```
 
## Examples

TODO
"""

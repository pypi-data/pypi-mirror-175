YOLOv4 darknet by OpenCV DNN.


Install package
```
pip install yolov4-cv
```


Code example:

```python
import numpy as np
from yolov4_cv import YOLOv4_CV
import cv2


# Just inherit YOLOv4_CV and define your class_names and class_colors
class YOLOv4(YOLOv4_CV):

    # Define coco class names
    class_names = [
        'person', 'bicycle', 'car', 'motorcycle', 'airplane', 
        'bus', 'train', 'truck', 'boat', 'traffic light', 
        'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 
        'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 
        'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 
        'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 
        'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 
        'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 
        'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 
        'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 
        'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 
        'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 
        'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 
        'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
    ]

    # Random to generate colors
    class_colors = [(int(i[0]), int(i[1]), int(i[2])) for i in np.random.randint(256, size=(len(class_names), 3))]


# Simple camera read
def load_capture():
    capture = cv2.VideoCapture(1)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    return capture


if __name__ == '__main__':
    # Load camera
    capture = load_capture()
    
    # Load checkpoint from any path. (onnx only)
    model = YOLOv4('tests/yolov4-tiny.weights', 'tests/yolov4-tiny.cfg', (416, 416))

    while True:
        # Get camera frame
        success, frame = capture.read()
        if not success:
            print('Open camera fail.')
            break

        # Inference all of output result
        preds = model(frame)
        for pred in preds:
            print(pred.id, pred.name, pred.conf, pred.box)

        # Show labeled box result
        model.show_label_boxes() 
        
        # or you can get labeled box result
        # img = model.get_label_boxes_image()

        # Any key to quit.
        if cv2.waitKey(1) > -1:
            print('finished by user')
            break

    capture.release()

```

Demo example:
![image info](./demo/sample.jpg)
import argparse
import sys
import time

import cv2
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision
import utils

# Initialize the object detection model
base_options = core.BaseOptions(
    file_name='model/efficientdet_lite0.tflite', use_coral=False, num_threads=4)
detection_options = processor.DetectionOptions(
    max_results=5, score_threshold=0.3)
options = vision.ObjectDetectorOptions(
    base_options=base_options, detection_options=detection_options)
detector = vision.ObjectDetector.create_from_options(options)

def detect(image):
    image = cv2.flip(image, 1)
    # Convert the image from BGR to RGB as required by the TFLite model.
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Create a TensorImage object from the RGB image.
    input_tensor = vision.TensorImage.create_from_array(rgb_image)
    detection_result = detector.detect(input_tensor)
    return detection_result

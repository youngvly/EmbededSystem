
from flask import Flask, request
from flask import render_template
import RPi.GPIO as gpio
import time
import cv2
import argparse
import io
import re

gpio.setmode(gpio.BCM)
gpio.setup(4,gpio.IN)
cam = cv2.VideoCapture(0)

app = Flask(__name__)

#detected = False

def motionSensing() :
   # while True:
        try:
            #print(",,,")
            if gpio.input(4) == 1:
                print("motion detected!!")
                return True
            else :
                print("nobody here")
                return False
        except KeyboardInterrupt :
            gpio.cleanup()
            cam.release()

# [START vision_label_detection]
def detect_labels(path):
    """Detects labels in the file."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    # [START vision_python_migration_label_detection]
    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations
    #print('Labels:')
    
    return labels
    #for label in labels:
    #    print(label.description)
    # [END vision_python_migration_label_detection]
# [END vision_label_detection]

@app.route("/detecting")
def main():
    
    isdetected = {
        'detected' : motionSensing()
        }
    return render_template('main.html', **isdetected)

@app.route("/camera")
def camera() :
    imgName = "static/capturedImage.jpg"
    ret,im = cam.read()
    cv2.imwrite(imgName,im)
    things = {
        "labels" : detect_labels(imgName),
        "imgsrc" : imgName
    }
    #print(labels)
    return render_template('Camera.html',**things)
    


if __name__ == "__main__":
    app.run(host='192.168.0.4', port=8888)

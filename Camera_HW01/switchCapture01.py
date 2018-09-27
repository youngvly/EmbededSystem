#switch capture v01 - using GPIO

import RPi.GPIO as gpio
import time
import picamera

switch_pin = 12
gpio.setmode(gpio.BCM)
gpio.setup(switch_pin,gpio.IN,gpio.PUD_UP)

def button() :
    isClicked = False
    if gpio.input(switch_pin) == 0 :
        isClicked = True
    return isClicked

def capture() :
    with picamera.PiCamera() as camera :
        #camera.resolution(1024,768)
        camera.start_preview()
        time.sleep(1)
        camera.capture('capturedImage1.jpg',resize=(320,240))

try :
    while True:
        if button() == True:
            print("Switch ON")
            capture()
            time.sleep(0.5)
        else :
            print("Switch OFF")
            time.sleep(0.5)
except KeyboardInterrupt :
    gpio.cleanup()
    
    
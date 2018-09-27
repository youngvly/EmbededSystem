#set driver -> sudo modprobe bcm-v4l2

import cv2
import numpy as np
import RPi.GPIO as gpio
import time
import thread

led_pin = 19
gpio.setmode(gpio.BCM)
gpio.setup(led_pin,gpio.OUT)
blink = False

#get difference between 3 captured image
def diffImage(i):
    diff0 = cv2.absdiff(i[0], i[1])
    diff1 = cv2.absdiff(i[1], i[2])
    return cv2.bitwise_and(diff0, diff1) #calculate bit AND 

def getGrayCameraImage(cam):
    img=cam.read()[1] #cam.read() returns [boolean,image object]
    gimg=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gimg

def updateCameraImage(cam, i):
    i[0] = i[1]
    i[1] = i[2]
    i[2] = getGrayCameraImage(cam)

def ledBlink(delay):
    blink = True
    count = 1
    while count <=20 :
        gpio.output(led_pin,True)
        time.sleep(delay)
        gpio.output(led_pin,False)
        time.sleep(delay)
        count+=1
    blink = True
        
# setup video capture
if __name__ == "__main__":
    thresh = 32
    cam = cv2.VideoCapture(0)
    i = [None, None, None]
    for n in range(3):
        i[n] = getGrayCameraImage(cam)

    while True:
        diff = diffImage(i)
        ret,thrimg=cv2.threshold(diff, thresh, 1, cv2.THRESH_BINARY) #upper than thresh : 1 / other : 0
        #cv2.imshow('thres',thrimg)
        count = cv2.countNonZero(thrimg)
        if (count > 20):
            nz = np.nonzero(thrimg)
            cv2.rectangle(diff,(min(nz[1]),min(nz[0])),(max(nz[1]),max(nz[0])),(255,0,0),2) #draw box
            cv2.rectangle(i[0],(min(nz[1]),min(nz[0])),(max(nz[1]),max(nz[0])),(0,0,255),2)
            cv2.imwrite('detect.jpg',i[0])
            #ledBlink(0.5)
            if blink == False : 
                thread.start_new_thread(ledBlink,(0.5,))

        cv2.imshow('Detecting Motion', diff)

        # process next image
        updateCameraImage(cam, i)

        key = cv2.waitKey(10)
        print(key)
        if key == 27: # ascii code for 'ESC'
            gpio.output(led_pin,False)
            break
    
    cam.release()
    cv2.destroyAllWindows()
    


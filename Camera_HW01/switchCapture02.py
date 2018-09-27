import cv2
import RPi.GPIO as gpio
import time

switch_pin = 12
gpio.setmode(gpio.BCM)
gpio.setup(switch_pin,gpio.IN,gpio.PUD_UP)

cam = cv2.VideoCapture(0)

def button() :
    isClicked = False
    if gpio.input(switch_pin) == 0 :
        isClicked = True
    return isClicked

while True:
    ret,im = cam.read()
    cv2.imshow('video test',im)
    key = cv2.waitKey(10) #millisec wait
    
    if key == ord('x') : 
        break 
    if button(): 
        cv2.imwrite('captureImage2.jpg',im)
cam.release()
cv2.destroyAllWindows()

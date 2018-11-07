import RPi.GPIO as GPIO
import time
import cv2
import datetime
import io
import thread

from google.cloud import vision
from google.cloud.vision import types

ledGreen = 19
ledYellow = 20
ledRed = 21

GPIO.setmode(GPIO.BCM)

GPIO.setup(ledGreen,GPIO.OUT)
GPIO.setup(ledYellow,GPIO.OUT)
GPIO.setup(ledRed,GPIO.OUT)
GPIO.setup(12, GPIO.IN, GPIO.PUD_UP)
GPIO.setwarnings(False)

cam = cv2.VideoCapture(0)


def ledOn(color) :
    GPIO.output(color,True)
    time.sleep (5)
    GPIO.output(color,False)

def button():
    state = False
    if GPIO.input(12) == 0:
        state = True
        print("button press")
    return state

def camera():
    try:
        while True:
            ret, img = cam.read()
            cv2.imshow('Cam', img)
            
            key = cv2.waitKey(10)
            if key == 27:
            	cam.release()
            	cv2.destroyAllWindows()
            	GPIO.cleanup()
            	break

            if button() == True:
                filename = getDatetime() + '.jpg'
                cv2.imwrite(filename , img)
                time.sleep(0.5)
                detect_faces(filename)
		
    except KeyboardInterrupt:
        cam.release()
        cv2.destroyAllWindows()
        GPIO.cleanup()

def getDatetime():
    date = datetime.datetime.now()
    year = str(date.year)
    month = str(date.month)
    day = str(date.day)
    hour = str(date.hour)
    min = str(date.minute)
    sec = str(date.second)

    if int(month) < 10:
        month = '0' + month
    if int(day) < 10:
        day = '0' + day
    if int(hour) < 10:
        hour = '0' + hour
    if int(min) < 10:
        min = '0' + min

    t =  year + month + day + hour + min + sec

    return t

def detect_faces(path):
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    response = client.face_detection(image=image)
    faces = response.face_annotations
    
   # Names of likelihood from google.cloud.vision.enums
    likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')
    print('Faces:')

    for face in faces:
        print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in face.bounding_poly.vertices])

        print('face bounds: {}'.format(','.join(vertices)))
        
    if format(likelihood_name[face.anger_likelihood]) in likelihood_name[3:5:1]:
        thread.start_new_thread(ledOn,(ledRed,))
    elif format(likelihood_name[face.joy_likelihood]) in likelihood_name[3:5:1]:
        thread.start_new_thread(ledOn,(ledGreen,))
    elif format(likelihood_name[face.surprise_likelihood]) in likelihood_name[3:5:1]:
        thread.start_new_thread(ledOn,(ledYellow,))
        
if __name__ == '__main__':
    GPIO.output(ledRed,False)
    GPIO.output(ledGreen,False)
    GPIO.output(ledYellow,False)
    camera()



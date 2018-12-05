import time
import cv2
import datetime
import io
import os
import numpy
from threading import Timer,Thread,Event


from google.cloud import vision
from google.cloud.vision import types

class perpetualTimer():

    def __init__(self,t,hFunction,imgs):
      self.t=t
      self.hFunction = hFunction
      self.img = imgs
      self.thread = Timer(self.t,self.handle_function)
      self.cntJoy,self.cntAnger,self.cntSurprise = 0,0,0
      #print(imgs)

    def handle_function(self):
      self.cntJoy,self.cntAnger,self.cntSurprise = self.hFunction(self.img)
      self.thread = Timer(self.t,self.handle_function)
      self.thread.start()

    def start(self):
      self.thread.start()

    def cancel(self):
      self.thread.cancel()
      self.thread.join()
      
    def setImg (self,imgs) :
        #print("setImg : " ,imgs)
        self.img = imgs
    def getFaceCnt(self) :
        return {"joy" : self.cntJoy,
                "anger" : self.cntAnger,
                "surprise" : self.cntSurprise
                }


class SetCam() :
    filename = 'Resources/FaceCapture/video.avi'
    cam = cv2.VideoCapture(0)
        
    frames_per_second = 24.0
    res = '480p'

    # Standard Video Dimensions Sizes
    STD_DIMENSIONS =  {
        "480p": (640, 480),
        "720p": (1280, 720),
        "1080p": (1920, 1080),
        "4k": (3840, 2160),
    }
    
    # Video Encoding, might require additional installs
    # Types of Codes: http://www.fourstopFlag = Event()

    VIDEO_TYPE = {
        'avi' : cv2.cv.CV_FOURCC(*'XVID')
        #'avi': cv2.VideoWriter_fourcc(*'XVID'),
        #'mp4': cv2.VideoWriter_fourcc(*'H264'),
        #'mp4': cv2.VideoWriter_fourcc(*'XVID'),
    }
        
    #def __init__(self):
        
    # Set resolution for the video capture
    # Function adapted from https://kirr.co/0l6qmh
    def change_res(self,cam, width, height):
        self.cam.set(3, width)
        self.cam.set(4, height)

    # grab resolution dimensions and set video capture to it.
    def get_dims(self,cam, res='1080p'):
        width, height = self.STD_DIMENSIONS["480p"]
        if res in self.STD_DIMENSIONS:
            width,height = self.STD_DIMENSIONS[res]
        ## change the current caputre device
        ## to the resulting resolution
        self.change_res(cam, width, height)
        return width, height

    def get_video_type(self,filename):
        filename, ext = os.path.splitext(filename)
        if ext in self.VIDEO_TYPE:
          return  self.VIDEO_TYPE[ext]
        return self.VIDEO_TYPE['avi']


def camera():
    
    global img
    setcam = SetCam()
    p = perpetualTimer(5,detect_faces)
    try:
        out = cv2.VideoWriter(setcam.filename, setcam.get_video_type(setcam.filename), 25, setcam.get_dims(setcam.cam, setcam.res))
        p.start()
        while True:
            ret, img = setcam.cam.read()
            cv2.imshow('Cam', img)
            out.write(img)
            key = cv2.waitKey(10)
            if key == 27:
                setcam.cam.release()
                out.release()
                cv2.destroyAllWindows()
                p.cancle()
                break
            """time.sleep(1)
            filename = getDatetime() + '.jpg'
            cv2.imwrite(filename , img)
            time.sleep(0.5)
            detect_faces(filename)
            break"""
		
    except KeyboardInterrupt:
        setcam.cam.release()
        out.release()
        cv2.destroyAllWindows()

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
"""
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
        print("Anger")
        cntAnger += 1
    elif format(likelihood_name[face.joy_likelihood]) in likelihood_name[3:5:1]:
        print("Joy")
        cntJoy +=1
    elif format(likelihood_name[face.surprise_likelihood]) in likelihood_name[3:5:1]:
        print("Surprise")
        cntSurprise += 1
        """
cntJoy,cntAnger,cntSurprise,filecnt = 0 ,0 ,0 ,0

def detect_faces(imgs):
    global cntJoy,cntAnger,cntSurprise
    
    imgs = numpy.array(imgs)
    client = vision.ImageAnnotatorClient()
    cv2.imwrite('Resources/FaceCapture/'+str(filecnt) + '.jpg' , imgs)
    with io.open('Resources/FaceCapture/'+str(filecnt) + '.jpg', 'rb') as image_file:
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
        
        if format(likelihood_name[face.anger_likelihood]) in likelihood_name[3::1]:
            print("Anger")
            cntAnger += 1
            cv2.imwrite('Resources/FaceCapture/Anger.jpg' , imgs)
        elif format(likelihood_name[face.joy_likelihood]) in likelihood_name[3::1]:
            print("Joy")
            cntJoy +=1
            cv2.imwrite('Resources/FaceCapture/Joy.jpg' , imgs)
        elif format(likelihood_name[face.surprise_likelihood]) in likelihood_name[3::1]:
            print("Surprise")
            cntSurprise += 1
            cv2.imwrite('Resources/FaceCapture/Surprise.jpg' , imgs)
    return cntJoy,cntAnger,cntSurprise
            
def faceScore() :
    summary = cntJoy + cntAnger + cntSurprise
    
    PercentJoy = cntJoy/summary * 100
    
if __name__ == '__main__':
    
    camera()



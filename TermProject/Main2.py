#!/usr/bin/env bash
import cv2
import Tkinter as tk
import threading
import time

from PIL import Image, ImageTk
from FaceDetectGoogle import detect_faces,perpetualTimer,SetCam,faceScore
from Speech import detectSpeech,timeout,afterTimeout
from Word2 import wordExtract
from ScoreCalc import calcScore


## 20181210 self.out error Maybe.. -> Context scratch buffers could not be allocated due to unknown size.
class MainWindow :
    def __init__(self,window):
        self.window  = window #Makes main window
        self.window.title("WebCamTest")
        #self.window.config(background="#FFFFFF")
        #self.window.geometry('650x550')
        
        self.speechFilename = "Resources/speech.txt"
                
        self.vid = MyVideoCapture(0)
        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()
        
        self.startbutton=tk.Button(window, text="Start", width=50, command=self.start)
        self.startbutton.pack(anchor=tk.CENTER, expand=True)
        
        #variable
        self.setcam = SetCam(self.vid.vid)
        self.out = cv2.VideoWriter(self.setcam.filename,
                                       self.setcam.get_video_type(self.setcam.filename),
                                       25, self.setcam.get_dims(self.setcam.cam, self.setcam.res))
        #stop recording
        self.out.release()
        self.txtfile = open(self.speechFilename,'w')
        self.t =  threading.Thread(name='detectSpeech', target=detectSpeech, args=(self.txtfile,))
        ret,img = self.vid.get_frame()
        self.p = perpetualTimer(2,detect_faces,img)
        self.timeoutThread = threading.Timer(64,self.raiseTimeout)
        self.writeVideo = True
        
        
        self.delay = 25
        self.update()
                
        self.window.mainloop()
        
    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()
        self.p.setImg(frame)
        if ret:
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)

        self.window.after(self.delay, self.update)
            
    def raiseTimeout(self) :
        timeout()
        self.stop()

    def showtop5 (self,frames) :
        self.top5 = wordExtract(speechFilename)
        i=1
        if len(top5) == 0 :
            print("speech not detected (top5 is null)")
        for top in top5 :
            form = top[0] + " : "  + str(top[1])
            print(form)
            l = tk.Label(frames,text = form,height=20)
            #l.grid(row=1,column=0,rowspan=3,columnspan=2,sticky = tk.E+tk.N+tk.S)
            l.pack()
            l.place(height=30 , y = 50 +30*i)
            i +=1
            
    def showScore (self,frames) :
        #calculate totalScore
        totalscore = calcScore(faceCnt,self.top5)
        score = tk.Label(frames,text = totalscore,height=20)
        score.pack()

    def clearFrame(self,frames) :
        list = frames.grid_slaves()
        for l in list:
            l.destroy()
            
    def start(self):
        #global out,p,t, writeVideo,txtfile,timeoutThread
        #write new video
        
        try :
            
            self.writeVideo = True
            #print(writeVideo)
            #start detect_face 2seconds
            self.p.start()
            #start detecting Speech         
            self.t.start()                
            self.timeoutThread.start()
            
            self.startbutton["text"] = "Stop"
            self.startbutton["command"] = self.stop
            print("Started")
        except Exception as e:
            self.stop()
        
        
    def stop(self) :
        self.out = cv2.VideoWriter(self.setcam.filename,
                                       self.setcam.get_video_type(self.setcam.filename),
                                       25, self.setcam.get_dims(self.setcam.cam, self.setcam.res))
        #global writeVideo , faceCnt,timeoutThread,p
        self.writeVideo = False
        self.startbutton["text"] = "start"
        self.startbutton["command"] = self.start
        #stop recording
        self.out.release()
        #stop detect_face
        self.p.cancel()
        faceCnt = self.p.getFaceCnt()
        time.sleep(2)
        #stop detect_speech ( raise Exception)
        self.timeoutThread.cancel() #stop timer thread
        timeout()
        self.t.join()
        
        self.txtfile.close()
        self.resultwindow = newResultWindow()
        self.showtop5(self.resultwindow.wordFrame)
        self.showScore(self.resultwindow.scoreFrame)
        
        print(faceCnt)
        print("Stoped")


class newResultWindow :
    
    def __init__(self,videoPath = "./Resources/FaceCapture/video.avi") :
        
        self.resultWindow = tk.Toplevel(window)
        self.resultWindow.wm_title("Your Result")
        self.resultWindow.config(background="#FFFFFF")
        #self.resultWindow.geometry('640x550')
        
        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(videoPath)

        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(self.resultWindow, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()

        #scoreFrame
        self.scoreFrame = tk.Frame(self.resultWindow,width = self.vid.width, height = self.vid.height,bg = "snow2")
        self.scoreFrame.pack(anchor=tk.CENTER, expand=True)
        #self.scoreFrame.grid(row = 1,column=0)
        
        #wordFrame
        self.wordFrame = tk.Frame(self.resultWindow,width = self.vid.width, height = self.vid.height,bg = "snow2")
        self.scoreFrame.pack(anchor=tk.CENTER, expand=True)
        #self.wordFrame.grid(row = 2,column=0)
        
        self.delay = 15
        self.update()

        self.resultWindow.mainloop()
        
    def update(self):
        # Get a frame from the video source
         ret, frame = self.vid.get_frame()

         if ret:
            self.photo = mageTk.PhotoImage(image = Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)

         self.window.after(self.delay, self.update)


class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
        
        

if __name__ == '__main__' :
    try :
        global window
        window = tk.Tk()
        w = MainWindow(window)
        #MyVideoCapture(0)
    except KeyboardInterrupt :
        w.stop()


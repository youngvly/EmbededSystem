#!/usr/bin/env bash

import numpy as np
import cv2
import Tkinter as tk
import threading
import time
import gi
gi.require_version('Gst', '1.0')
gi.require_version('GObject', '2.0')
from gi.repository import GLib, GObject, Gst


#import pygst
#import gobject

from PIL import Image, ImageTk
import imageio
from FaceDetectGoogle import detect_faces,perpetualTimer,SetCam,faceScore
from Speech import detectSpeech,timeout,afterTimeout
from Word2 import wordExtract
from ScoreCalc import calcScore


#Set up GUI
window = tk.Tk()  #Makes main window
window.wm_title("WebCamTest")
window.config(background="#FFFFFF")
window.geometry('650x550')

#Graphics window
imageFrame = tk.Frame(window, width=640, height=480)
imageFrame.grid(row=0, column=0, padx=10, pady=2)

#button
secondFrame = tk.Frame(window,width=600,height=200,bg = "snow2")
secondFrame.grid(row=1,column=0,rowspan=3,columnspan=2,sticky=tk.W+tk.E+tk.N+tk.S,pady=10)


#Capture video frames
lmain = tk.Label(imageFrame)
lmain.grid(row=0, column=0)
setcam = SetCam()

speechFilename = "Resources/speech.txt"

def raiseTimeout() :
    timeout()
    stop()

def show_cam():
    global img , writeVideo
    ret, img = setcam.cam.read()
    
    if writeVideo == True :
        #print("writeVideo True")
        out.write(img)
        p.setImg(img)
    #print(writeVideo)
    img = cv2.flip(img, 1)
    cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_cam)
    
def showtop5 (frames) :
    global top5
    top5 = wordExtract(speechFilename)
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
def showScore (frames) :
    #calculate totalScore
    global top5
    totalscore = calcScore(faceCnt,top5)
    score = tk.Label(frames,text = totalscore,height=20)
    score.pack()

def clearFrame(frames) :
    list = frames.grid_slaves()
    for l in list:
        l.destroy()
        
def start():
    global out,p,t, writeVideo,txtfile,timeoutThread
    #write new video
    
    try :
        out = cv2.VideoWriter(setcam.filename, setcam.get_video_type(setcam.filename), 25, setcam.get_dims(setcam.cam, setcam.res))
        writeVideo = True
        #print(writeVideo)
        #start detect_face 2seconds
        p = perpetualTimer(2,detect_faces,img)
        p.start()
        #start detecting Speech
        txtfile = open(speechFilename,'w')
        t =  threading.Thread(name='detectSpeech', target=detectSpeech, args=(txtfile,))
        t.start()
        
        timeoutThread = threading.Timer(64,raiseTimeout)
        timeoutThread.start()
        
        startbutton["text"] = "Stop"
        startbutton["command"] = stop
        print("Started")
    except Exception as e:
        stop()
    
    
def stop() :
    global writeVideo , faceCnt,timeoutThread
    writeVideo = False
    startbutton["text"] = "start"
    startbutton["command"] = start
    #stop recording
    out.release()
    #stop detect_face
    p.cancel()
    faceCnt = p.getFaceCnt()
    time.sleep(2)
    #stop detect_speech ( raise Exception)
    timeoutThread.cancel() #stop timer thread
    timeout()
    t.join()
    
    txtfile.close()
    resultwindow = newResultWindow()
    showtop5(resultwindow.wordFrame)
    showScore(resultwindow.scoreFrame)
    
    print(faceCnt)
    print("Stoped")


class newResultWindow :
    
    def __init__(self) :
        
        self.resultWindow = tk.Toplevel(window)
        self.resultWindow.wm_title("Your Result")
        self.resultWindow.config(background="#FFFFFF")
        self.resultWindow.geometry('640x550')
        #videoFrame
        self.videoFrame = tk.Frame(self.resultWindow,width=600,height=200,bg = "snow2")
        self.videoFrame.grid(row = 0,column=0)
        self.videoLabel = tk.Label(self.videoFrame)
        self.videoLabel.pack()
        #scoreFrame
        self.scoreFrame = tk.Frame(self.resultWindow,width=600,height=200,bg = "snow2")
        self.scoreFrame.grid(row = 1,column=0)
        
        #wordFrame
        self.wordFrame = tk.Frame(self.resultWindow,width=600,height=200,bg = "snow2")
        self.wordFrame.grid(row = 2,column=0)
        #buttonFrame
        #buttonFrame = tk.Frame(window,width=600,height=200,bg = "snow2")
        #buttonFrame.grid(row = 3,column=0)
        
        videoThread = threading.Thread(target=self.showVideo)
        videoThread.daemon = 1
        videoThread.start()
        
        #ffmpeg
        imageio.plugins.ffmpeg.download()

    def showVideo (self):
        #OSError: [Errno 8] Exec format error
        #videoPath = "/home/pi/EmbededSystem/TermProject/Resources/FaceCapture/video.avi"
        videoPath = "./Resources/FaceCapture/video.avi"
        video = imageio.get_reader(videoPath)
        for image in video.iter_data() :
            frame_image = ImageTK.PhotoImage(Image.fromarray(image))
            label.config(image=frame_image)
            label.image = frame_image


        

startbutton = tk.Button(secondFrame,text="Start" ,width=50, command = start)
startbutton.place(relx=0.5, rely=0.1, anchor=tk.CENTER)


if __name__ == '__main__' :
    writeVideo = None

    try :
        show_cam()  #Display 2
        window.mainloop()  #Starts GUI
    except KeyboardInterrupt :
        stop()
        

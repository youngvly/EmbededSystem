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
    totalscore = calcScore(faceCnt,top5)
    score = tk.Label(frames,text = totalscore,height=20)
    score.pack()

def clearFrame(frames) :
    list = frames.grid_slaves()
    for l in list:
        l.destroy()
        
def start():
    global out,p,t, writeVideo,txtfile
    #write new video
    out = cv2.VideoWriter(setcam.filename, setcam.get_video_type(setcam.filename), 25, setcam.get_dims(setcam.cam, setcam.res))
    writeVideo = True
    #print(writeVideo)
    #start detect_face 5seconds
    p = perpetualTimer(5,detect_faces,img)
    p.start()
    #start detecting Speech
    txtfile = open(speechFilename,'w')
    t =  threading.Thread(name='detectSpeech', target=detectSpeech, args=(txtfile,))
    t.start()
    startbutton["text"] = "Stop"
    startbutton["command"] = stop
    
    clearFrame(secondFrame)
    clearFrame(thirdFrame)
    print("Started")
    
def stop() :
    global writeVideo , faceCnt
    writeVideo = False
    startbutton["text"] = "start"
    startbutton["command"] = start
    #stop recording
    out.release()
    #stop detect_face
    p.cancel()
    faceCnt = p.getFaceCnt()
    time.sleep(2)
    #stop detect_speech
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
        #scoreFrame
        self.scoreFrame = tk.Frame(self.resultWindow,width=600,height=200,bg = "snow2")
        self.scoreFrame.grid(row = 1,column=0)
        
        #wordFrame
        self.wordFrame = tk.Frame(self.resultWindow,width=600,height=200,bg = "snow2")
        self.wordFrame.grid(row = 2,column=0)
        #buttonFrame
        #buttonFrame = tk.Frame(window,width=600,height=200,bg = "snow2")
        #buttonFrame.grid(row = 3,column=0)
        videoPath = "/home/pi/EmbededSystem/TermProject/Resources/FaceCapture/video.avi"
        self.showVideo(videoPath)
        
    def on_sync_message(self,bus, message, window_id):
        if not message.structure is None:
            if message.structure.get_name() == 'prepare-xwindow-id':
                image_sink = message.src
                image_sink.set_property('force-aspect-ratio', True)
                image_sink.set_xwindow_id(window_id)

    def showVideo (self,filename):
        GObject.threads_init()
        Gst.init(None)
        #self.videoFrame.pack(side=tk.BOTTOM,anchor=tk.S,expand=tk.YES,fill=tk.BOTH)

        window_id = self.videoFrame.winfo_id()

        player = Gst.ElementFactory.make('playbin','player')
        #player = Gst.element_factory_make('playbin2', 'player')
        player.set_property('video-sink', None)
        player.set_property('uri', 'file://%s' % (filename))
        player.set_state(Gst.State.PLAYING)

        bus = player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect('sync-message::element', self.on_sync_message, window_id)

startbutton = tk.Button(secondFrame,text="Start" ,width=50, command = start)
startbutton.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

#thirdFrame = tk.Frame(window,width=300,height = 800,bg = "snow3")
#thirdFrame.grid(row=0,column=3,rowspan=5,columnspan=1,sticky = tk.E+tk.N+tk.S)
#l = tk.Label(thirdFrame,text = "WordFrequency Top5",height=20)
#l.grid(row=1,column=0,rowspan=3,columnspan=2,sticky = tk.E+tk.N+tk.S)
#l.pack()
#l.place(height=50)




#Slider window (slider controls stage position)
#sliderFrame = tk.Frame(window, width=600, height=100)
#sliderFrame.grid(row = 600, column=0, padx=10, pady=2)

if __name__ == '__main__' :
    writeVideo = None

    try :
        show_cam()  #Display 2
        window.mainloop()  #Starts GUI
    except KeyboardInterrupt :
        stop()
        

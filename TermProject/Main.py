import numpy as np
import cv2
import Tkinter as tk
from PIL import Image, ImageTk
from FaceDetectGoogle import detect_faces,perpetualTimer,SetCam,faceScore
from Speech import detectSpeech
#Set up GUI
window = tk.Tk()  #Makes main window
window.wm_title("WebCamTest")
window.config(background="#FFFFFF")
window.geometry('900x800')

#Graphics window
imageFrame = tk.Frame(window, width=640, height=480)
imageFrame.grid(row=0, column=0, padx=10, pady=2)

#Capture video frames
lmain = tk.Label(imageFrame)
lmain.grid(row=0, column=0)
setcam = SetCam()


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
    
def start():
    global out,p , writeVideo
    #write new video
    out = cv2.VideoWriter(setcam.filename, setcam.get_video_type(setcam.filename), 25, setcam.get_dims(setcam.cam, setcam.res))
    writeVideo = True
    #print(writeVideo)
    #start detect_face 5seconds
    p = perpetualTimer(5,detect_faces,img)
    p.start()
    startbutton["text"] = "Stop"
    startbutton["command"] = stop
    print("Started")
    
def stop() :
    global writeVideo
    writeVideo = False
    startbutton["text"] = "start"
    startbutton["command"] = start
    #stop recording
    out.release()
    #stop detect_face
    p.cancel()
    print("Stoped")
    
#button
secondFrame = tk.Frame(window,width=600,height=400,bg = "snow2")
secondFrame.grid(row=1,column=0,rowspan=3,columnspan=2,sticky=tk.W+tk.E+tk.N+tk.S)
startbutton = tk.Button(secondFrame,text="Start" ,width=50, command = start)
startbutton.place(relx=0.5, rely=0.1, anchor=tk.CENTER)


#thirdFrame
thirdFrame = tk.Frame(window,width=300,height = 800,bg = "snow3")
thirdFrame.grid(row=0,column=3,rowspan=3,columnspan=2,sticky = tk.E+tk.N+tk.S)

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
        

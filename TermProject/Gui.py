import numpy as np
import cv2
import Tkinter as tk
from PIL import Image, ImageTk

#Set up GUI
window = tk.Tk()  #Makes main window
window.wm_title("WebCamTest")
window.config(background="#FFFFFF")
window.geometry('900x800')

#Graphics window
imageFrame = tk.Frame(window, width=600, height=400)
imageFrame.grid(row=0, column=0, padx=10, pady=2)

#Capture video frames
lmain = tk.Label(imageFrame)
lmain.grid(row=0, column=0)
cam = cv2.VideoCapture(0)
def show_frame():
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame) 

#button
secondFrame = tk.Frame(window,width=600,height=400,bg = "snow2")
secondFrame.grid(row=1,column=0,rowspan=3,columnspan=2,sticky=tk.W+tk.E+tk.N+tk.S)
startbutton = tk.Button(secondFrame,text="Start" ,width=50)
startbutton.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

#thirdFrame
thirdFrame = tk.Frame(window,width=300,height = 800,bg = "snow3")
thirdFrame.grid(row=0,column=3,rowspan=3,columnspan=2,sticky = tk.E+tk.N+tk.S)

#Slider window (slider controls stage position)
#sliderFrame = tk.Frame(window, width=600, height=100)
#sliderFrame.grid(row = 600, column=0, padx=10, pady=2)


show_frame()  #Display 2
window.mainloop()  #Starts GUI
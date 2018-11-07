import cv2
import glob
import time
faceDet = cv2.CascadeClassifier("OpenCV_FACE/haarcascade_frontalface_default.xml")
#emotions = ["surprise"]
def detect_faces():
    start = time.time()
    files = glob.glob("exImage/rawImage/*" ) #Get list of all images with emotion
    filenumber = 0
    for f in files:
        frame = cv2.imread(f) #Open image
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #Convert image to grayscale
        #Detect face using 4 different classifiers
        face = faceDet.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)
        if len(face) == 1:
            facefeatures = face
        else:
            facefeatures = ""
        #Cut and save face
        for (x, y, w, h) in facefeatures: #get coordinates and size of rectangle containing face
            print "face found in file: %s" %f
            gray = gray[y:y+h, x:x+w] #Cut the frame to size
            try:
                out = cv2.resize(gray, (350, 350)) #Resize face so all images have same size
                cv2.imwrite("exImage/faceExtract/%s.jpg" %(filenumber), out) #Write image
            except:
               pass #If error, pass file
        filenumber += 1 #Increment image number
    end = time.time()
    print("Extract Face 10img Time:" , end-start)
#detect_faces() #Call functiona
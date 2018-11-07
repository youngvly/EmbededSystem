import cv2
import glob
import random
import numpy as np
import time
from FaceExtract2 import detect_faces

#emotions = ["neutral", "anger", "contempt", "disgust", "fear", "happy", "sadness", "surprise"] #Emotion list
emotions = ["anger", "happy"] #Emotion list
fishface = cv2.createFisherFaceRecognizer() #Initialize fisher face classifier
data = {}
def get_Training_files(emotion): #Define function to get file list, randomly shuffle it and split 80/20
    files = glob.glob("dataset/%s/*" %emotion)
    random.shuffle(files)
    training = files[:int(len(files)*0.8)] #get first 80% of file list
    return training
def get_Test_files():
    detect_faces()
    files = glob.glob("exImage/faceExtract/*")
    return files

def make_sets():
    training_data = []
    training_labels = []
    prediction_data = []
    prediction = get_Test_files()
    for emotion in emotions:
        training = get_Training_files(emotion)
        #Append data to training and prediction list, and generate labels 0-7
        for item in training:
            image = cv2.imread(item) #open image
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #convert to grayscale
            training_data.append(gray) #append image array to training data list
            training_labels.append(emotions.index(emotion))
        for item in prediction: #repeat above process for prediction set
            image = cv2.imread(item)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            prediction_data.append(gray)
    return training_data, training_labels, prediction_data

def run_recognizer():
    training_data, training_labels, prediction_data= make_sets()
    print "training fisher face classifier"
    start = time.time()
    fishface.train(training_data, np.asarray(training_labels))
    end = time.time()
    print("training Time:" , end-start)
    #print "predicting classification set"
    cnt = 0
    correct = 0
    incorrect = 0
    print "prediction"
    start = time.time()
    for image in prediction_data:
        pred, conf = fishface.predict(image)
        print(emotions[pred])
    end = time.time()
    print("predinct 10img Time:" , end-start)
    return 
#Now run it

run_recognizer()

    #print "got", correct, "percent correct!"
    #metascore.append(correct)
#print "\n\nend score:", np.mean(metascore), "percent correct!"

import io
import os

#Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

#instantiates a client
client = vision.ImageAnnotatorClient()

file_name = os.path.join(
    os.path.dirname(__file__), 'image.jpg')

#loads the image into memory
with io.open(file_name, 'rb') as image_file :
    content = image_file.read()

image = types.Image(content=content)

#Performs label detection on the image file
response = client.label_detection(image=image)
labels = response.label_annotations

print("labels  : ")
for label in labels :
    print (label.description)

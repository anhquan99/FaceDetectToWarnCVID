from PIL import Image
import os
import cv2


BASE_PATH = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_PATH, "images/2.jpg")

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
image = cv2.imread(image_dir)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(
    gray, 
    scaleFactor = 1.5, 
    minNeighbors = 5
)
print("face found {0}" .format(len(faces)))
for(x, y, w, h) in faces:
    cv2.rectangle(image, (x,y), (x+w,y+h), (0,255,0), 2)
scaleHeight = int(image.shape[1] / 2)
mywith = int(image.shape[0]/2)
myheight = int(image.shape[1]/2)
print(mywith , "   ", myheight)
# image = cv2.resize(image, (mywith, myheight))
cv2.imshow("face found", image)

cv2.waitKey(0)
for face in faces:
    print(face)
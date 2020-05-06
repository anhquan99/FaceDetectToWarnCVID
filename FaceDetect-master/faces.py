import cv2
import numpy as np
cap = cv2.VideoCapture(0)
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")  
while(True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray, 
        scaleFactor = 1.5,
        minNeighbors = 5
    )
    for(x,y,w,h) in faces:
        print(x,y,w,h)
    # cv2.imshow('gray', gray)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
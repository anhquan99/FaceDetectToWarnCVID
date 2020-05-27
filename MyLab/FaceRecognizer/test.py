import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
cap = cv2.VideoCapture(0)
while(True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces =  face_cascade.detectMultiScale(
        gray,
        scaleFactor = 1.5,
        minNeighbors = 5
    )
    for(x,y,w,h) in faces:
        print(x,y,w,h)
        #region of interest
        roi_gray = gray[y : y + h, x : x + w]
        roi_color = frame[y : y + h, x : x + w]
        
        #recognize depp learned model predict keras tensorflow pytorch scikit learn
        

        #file to save
        img_item = "my-image.png"
        img_item_color = 'my-image-color.png'
        
        #write file 
        cv2.imwrite(img_item_color, roi_color)  
        cv2.imwrite(img_item, roi_gray)

        #draw rectangle
        color = (0,255,0) #BGR
        stokes = 2
        end_cord_x = x + w
        end_cord_y = y + h
        cv2.rectangle(frame, (x,y), (end_cord_x,end_cord_y), color, stokes)
    cv2.imshow('frame', frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
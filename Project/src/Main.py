# import libraries
import os
import numpy as np
import cv2
import pickle
import imutils
import time  
import datetime
import pyodbc
# import classes
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils.video import FPS  
from pathlib import Path
# import local file
import JsonReader
import Analyzer
import FaceClass
import Repository

# paths
p = Path(__file__).parents[1]
dataDir = os.path.join(p, "data")
imageDir = os.path.join(p, "image")
modelDir = os.path.join(p, "model")

maskNetPath = os.path.sep.join([modelDir , "mask_detector.model"])
recognizerPath = os.path.sep.join([dataDir , "recognizer.pickle"])
lePath = os.path.sep.join([dataDir , "le.pickle"])

# files
protoPath = modelDir + "/deploy.prototxt"
modelPath = modelDir + "/res10_300x300_ssd_iter_140000.caffemodel"
embeddedPath = modelDir + "/openface_nn4.small2.v1.t7"

# params
le = pickle.loads(open(lePath, "rb").read())
recognizer = pickle.loads(open(recognizerPath, "rb").read())
embedder = cv2.dnn.readNetFromTorch(embeddedPath)
detector =cv2.dnn.readNetFromCaffe(protoPath, modelPath)
maskNet = load_model(maskNetPath)

# load json data 
initialParams = JsonReader.loadData()

#timer
timer = datetime.datetime.now().minute

# initial connection to database
conn = pyodbc.connect('Driver={SQL Server};'
                        'Server=DESKTOP-LO3H31I;'
                        'Database=PREDICT_COVID;'
                        'Trusted_Connection=yes;'
                        ,autocommit=True)
cursor = conn.cursor()
cursor.fast_executemany = True

# initialize Video Stream
vs = VideoStream(src=0).start()
time.sleep(2.0)
fps = FPS().start() 
# mid points 
def midpoint(ptA, ptB):
	return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)
# detected faces
analyzedFacesArr = []
while True:
    # current minute
    current = datetime.datetime.now().minute
    # take detected faces and reinit every loop
    detectedFacesArr = []
    # faces with and without detected
    faces = []

    frame = vs.read()
    # resize the frame to have a width of 600 pixels (while
	# maintaining the aspect ratio), and then grab the image
	# dimensions
    frame = imutils.resize(frame, width=600)
    (h, w) = frame.shape[:2]
    frameBlob = cv2.dnn.blobFromImage(
		cv2.resize(frame, (300, 300)), 1.0, (300, 300),
		(104.0, 177.0, 123.0))
    #, swapRB=False, crop=False
    # apply OpenCV's deep learning-based face detector to localize
	# faces in the input image
    detector.setInput(frameBlob)
    detections = detector.forward()
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        
        if confidence > 0.5:
            # color for frame detection
            color = (0,0,255)
            box = detections[0,0,i, 3:7] * np.array([w, h, w, h])
            # for face
            (startX,startY, endX, endY) = box.astype("int")
            # for mask
            (startXMask,startYMask, endXMask, endYMask) = box.astype("int")
            # face ROI
            faceROI = (startX, startY, endX, endY)
            faces.append(faceROI)
            face = frame[startX:endX, startY:endY]
            # face mask ROI
            faceMask = frame[startXMask:endXMask, startYMask:endYMask]
            (fH, fW) = face.shape[:2]
            # ensure the face width and height are sufficiently large
            if fW < 20 or fH < 20:
                continue
            
            # mask recognize
            # ensure the bounding boxes fall within the dimensions of
			# the frame
            (startXMask, startYMask) = (max(0, startX), max(0, startY))
            (endXMask, endYMask) = (min(w - 1, endX), min(h - 1, endY))
            # extract the face ROI, convert it from BGR to RGB channel
			# ordering, resize it to 224x224, and preprocess it
            # face = frame[startY:endY, startX:endX]
            faceMask = cv2.cvtColor(faceMask, cv2.COLOR_BGR2RGB)
            faceMask = cv2.resize(faceMask, (224,224))
            faceMask = img_to_array(faceMask)
            faceMask = preprocess_input(faceMask)
            faceMask = np.expand_dims(faceMask, axis=0)
            (mask, withoutMask) = maskNet.predict(faceMask)[0]
            if mask >= withoutMask:
                label = "Mask"
                color = (255, 0 ,0)
            else:
                label = "No Mask"

            # recognize face
            faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,
				(96, 96), (0, 0, 0), swapRB=True, crop=False)
            embedder.setInput(faceBlob)
            vec = embedder.forward()
            preds = recognizer.predict_proba(vec)[0]
            j = np.argmax(preds)
            proba = preds[j]
            name = le.classes_[j]
            text = ""
            # make sure probabilty is greater than 50%
            if proba * 100 > 55 and not FaceClass.isFaceExistedInDetected(name, detectedFacesArr):
                detectedFacesArr.append((faceROI,label,name))
                color = (0,255,0)
                text = "{}: {:.2f}%".format(name, proba * 100) 
 
            cv2.putText(frame,text + " " + label, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
            cv2.rectangle(frame, (startX,startY), (endX,endY),
                color,2)
    # calculate distance
    if len(faces) >= 2:
        avg = []
        for i in faces:
            # midpoint
            avgX = int(round(i[0] + i[2]) /2)
            avgY = int(round(i[1] + i[3]) /2)
            avgPx = int(round((i[2] - i[0])/initialParams["face_avg"]))
            avg.append((avgX, avgY,avgPx))
            # draw middle point
            frame = cv2.circle(frame, (avgX, avgY), radius=0, color=(0, 0, 255), thickness=5)
        # distance from reference face to other faces
        for i in range(0,len(avg)):
            currentDetectedFace = None
            # find reference face
            if FaceClass.findROIInDetectedFaces(faces[i], detectedFacesArr):
                currentDetectedFace =  FaceClass.findDetectedFace(faces[i], detectedFacesArr)
            # to other faces
            for p in range(i+1,len(avg)):
                # draw line
                cv2.line(frame, (avg[i][0], avg[i][1]), (avg[p][0], avg[p][1]), (0,0,255), 1)
                (m1, m2) = midpoint(avg[i], avg[p])
                # distance
                D = dist.euclidean(avg[i], avg[p]) / avg[i][2]
                # draw text
                cv2.putText(frame, "{:.1f}".format(D), (int(m1), int(m2 - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0,0,255), 1)
                # find other faces
                if FaceClass.findROIInDetectedFaces(faces[p], detectedFacesArr) and currentDetectedFace is not None:
                    otherDetectedFace = FaceClass.findDetectedFace(faces[p], detectedFacesArr)
                    # calculate percentage
                    percentage = Analyzer.analyzePercentByContactRange(D, currentDetectedFace[1], otherDetectedFace[1])
                    # if reference and other face already in analyzed face
                    analyzedFacesArr = Analyzer.analyzePredicted(analyzedFacesArr,
                        FaceClass.AnalyzedFaces(currentDetectedFace[2], 
                        otherDetectedFace[2], 
                        percentage,0))
        # print(analyzedFacesArr)
        # print(len(faces), " + ", len(avg) )
        
    if timer != current:
        # analyze wrong prediction and update database
        if len(analyzedFacesArr) > 0:
            analyzedFacesArr = Analyzer.analyzeWrongPrediction(analyzedFacesArr)
            Repository.addPredictionToDatabase(cursor, analyzedFacesArr)
            # reset analyzed face array
            analyzedFacesArr.clear()
        # update time
        timer = current      
        
    fps.update()
    cv2.imshow('frame', frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
fps.stop()
vs.stop()
cv2.destroyAllWindows()


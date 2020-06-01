# import os
# import numpy as np
# import cv2
# import pickle
# from pathlib import Path
# import imutils
# from imutils.video import VideoStream
# from imutils.video import FPS  
# import time  
# from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
# from tensorflow.keras.preprocessing.image import img_to_array
# from tensorflow.keras.models import load_model
# import JsonReader
# from scipy.spatial import distance as dist

# # paths
# p = Path(__file__).parents[1]
# dataDir = os.path.join(p, "data")
# modelDir = os.path.join(p, "model")

# # files
# protoPath = modelDir + "/deploy.prototxt"
# modelPath = modelDir + "/res10_300x300_ssd_iter_140000.caffemodel"
# maskNetPath = modelDir + "/mask_detector.model"

# # params
# initialParams = JsonReader.loadData()
# detector =cv2.dnn.readNetFromCaffe(protoPath, modelPath)
# maskNet = load_model(maskNetPath)
# vs = VideoStream(src=0).start()
# time.sleep(2.0)
# fps = FPS().start()

# # mid points 
# def midpoint(ptA, ptB):
# 	return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

# while True:
#     frame = vs.read()
#     # resize the frame to have a width of 600 pixels (while
# 	# maintaining the aspect ratio), and then grab the image
# 	# dimensions
#     frame = imutils.resize(frame, width=600)
#     (h, w) = frame.shape[:2]
#     imageBlob = cv2.dnn.blobFromImage(
# 		cv2.resize(frame, (300, 300)), 1.0, (300, 300),
# 		(104.0, 177.0, 123.0), swapRB=False, crop=False)
#     # apply OpenCV's deep learning-based face detector to localize
# 	# faces in the input image
#     detector.setInput(imageBlob)
#     detections = detector.forward()
#     faces = []
#     for i in range(0, detections.shape[2]):
#         confidence = detections[0, 0, i, 2]
        
#         if confidence > 0.5:
#             box = detections[0,0,i, 3:7] * np.array([w, h, w, h])
#             (startX,startY, endX, endY) = box.astype("int")

#             # face ROI
#             face = frame[startX:endX, startY:endY]
#             (fH, fW) = face.shape[:2]
#             # ensure the face width and height are sufficiently large
#             if fW < 20 or fH < 20:
#                 continue
#             faces.append(face)
#             faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,
#                 (96,96), (0,0,0), swapRB=True, crop=False)
#             # face = frame[startY:endY, startX:endX]
#             face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
#             face = cv2.resize(face, (224,224))
#             face = img_to_array(face)
#             face = preprocess_input(face)
#             face = np.expand_dims(face, axis=0)
#             (mask, withoutMask) = maskNet.predict(face)[0]
#             label = "Mask" if mask > withoutMask else "No Mask"

#             cv2.putText(frame, label, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0,0,255), 2)

#             cv2.rectangle(frame, (startX,startY), (endX,endY),
#                 (0,0,255),2)
#     if len(faces) >= 2:
#         avg = []
#         for i in faces:
#             avgX = int(round(i[0] + i[2]) /2)
#             avgY = int(round(i[1] + i[3]) /2)
#             avgPx = int(round((i[2] - i[0])/initialParams["face_avg"]))
#             avg.append((avgX, avgY,avgPx))
#             frame = cv2.circle(frame, (avgX, avgY), radius=0, color=(0, 0, 255), thickness=5)
#         for i in range(0,len(avg)):
#             for p in range(i+1,len(avg)):
#                 cv2.line(frame, (avg[i][0], avg[i][1]), (avg[p][0], avg[p][1]), (0,0,255), 1)
#                 (m1, m2) = midpoint(avg[i], avg[p])
#                 D = dist.euclidean(avg[i], avg[p]) / avg[i][2]
#                 print(D)
#                 cv2.putText(frame, "{:.1f}".format(D), (int(m1), int(m2 - 10)),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0,0,255), 1)   
#     fps.update()

#     cv2.imshow('frame', frame)
#     if cv2.waitKey(20) & 0xFF == ord('q'):
#         break
# fps.stop()
# vs.stop()
# cv2.destroyAllWindows()
import datetime
min = datetime.datetime.now().minute
print(min)

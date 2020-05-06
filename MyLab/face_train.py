import os
import numpy as np
import cv2
import pickle
from PIL import Image
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_PATH, "images")
#i don't know why this works
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()

current_id = 0
label_ids = {}
y_labels = []
x_train = []

for root , dirs, files in os.walk(image_dir):
    for file in files:
        if file.endswith("png") or file.endswith("jpg"):  
            path = os.path.join(root, file)
            image = Image.open(path)  
            # label = os.path.basename(os.path.dirname(path))
            label = os.path.basename(root).replace(" ", "-").lower()
            # print(label, path)
            if not label in label_ids:
                label_ids[label] = current_id
                current_id += 1
                print(current_id)
            id_ = label_ids[label]
            # print(label_ids)
            # y_lables.append(lable) #some number
            # x_train.append(path)    # varyfy this image, turn in to NUMPY arrays, gray
            pil_image = Image.open(path).convert('L') # grayscale
            size = (550, 550)
            final_image = pil_image.resize(size, Image.ANTIALIAS)
            image_array = np.array(final_image, "uint8")
            # print(image_array)
            faces = face_cascade.detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=5)
            for (x, y, w, h) in faces:
                # print(x, y, w, h)
                roi = image_array[y: y + h, x : x + w]
                x_train.append(roi)
                y_labels.append(id_)
# print(y_lables)
# print(x_train)
with open("label.pickle", "wb") as f:
    pickle.dump(label_ids, f)
recognizer.train(x_train, np.array(y_labels))
recognizer.save("trainner.yml")


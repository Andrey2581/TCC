import os
import face_recognition
import cv2
import json

image_folder = 'face_recognition\images'

folders = os.listdir(image_folder)
encodings = {}

for folder in folders:
    encodings[folder] = []
    path = os.path.join(image_folder, folder)
    files = os.listdir(path)
    for file in files:
        print('ok')
        if file.lower().endswith('.jpg') or file.lower().endswith('.jpeg'):
            image = cv2.imread(os.path.join(path, file))
            try:
                encodings[folder].append(
                    face_recognition.face_encodings(image)[0].tolist())
            except Exception:
                print("Face not detected")

with open('file_encoding.json', 'w') as file:
    json.dump(encodings, file)

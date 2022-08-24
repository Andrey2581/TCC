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
        if file.lower().endswith('.jpg'):
            image = cv2.imread(os.path.join(path, file))
            encodings[folder].append(
                face_recognition.face_encodings(image)[0].tolist())

with open('file_encoding.json', 'w') as file:
    json.dump(encodings, file)

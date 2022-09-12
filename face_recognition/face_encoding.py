import os
import face_recognition
import cv2
import json
import pymongo

mongo = pymongo.MongoClient("localhost")
db = mongo["tcc"]
collection = db["test"]

image_folder = 'face_recognition\images'
folders = os.listdir(image_folder)

for folder in folders:
    path = os.path.join(image_folder, folder)
    files = os.listdir(path)

    info = None
    encode = None

    for file in files:
        if file.lower().endswith('info.json'):
            with open(os.path.join(path, file), 'r') as f:
                info = json.load(f)
        if file.lower().endswith('.jpg') or file.lower().endswith('.jpeg'):
            image = cv2.imread(os.path.join(path, file))
            try:
                encode = face_recognition.face_encodings(image)[0].tolist()
            except Exception:
                print(f"Face not detected in file <{file}>")
        if encode != None and info != None:
            info["face_encoding"] = encode
            try:
                collection.insert_one(info)
            except Exception as e:
                print(f"Error: {e}")

mongo.close()

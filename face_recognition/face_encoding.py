import os
import face_recognition
import cv2
import json
import pymongo
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import shutil

# mongo = pymongo.MongoClient("localhost")
# db = mongo["tcc"]
# collection = db["test"]

# image_folder = 'face_recognition\images'
# folders = os.listdir(image_folder)

# for folder in folders:
#     path = os.path.join(image_folder, folder)
#     files = os.listdir(path)

#     info = None
#     encode = None

#     for file in files:
#         if file.lower().endswith('info.json'):
#             with open(os.path.join(path, file), 'r') as f:
#                 info = json.load(f)
#         if file.lower().endswith('.jpg') or file.lower().endswith('.jpeg'):
#             image = cv2.imread(os.path.join(path, file))
#             try:
#                 encode = face_recognition.face_encodings(image)[0].tolist()
#             except Exception:
#                 print(f"Face not detected in file <{file}>")
#         if encode != None and info != None:
#             info["face_encoding"] = encode
#             try:
#                 collection.insert_one(info)
#             except Exception as e:
#                 print(f"Error: {e}")

# mongo.close()


class Info(BaseModel):
    id: str
    name: str
    email: str


app = FastAPI()


@app.post('/')
def home(info: Info):
    return info


@app.post('/test/{id}/{name}/{email}')
async def test(id: str, name: str, email: str, file: UploadFile = File(...)):
    info = {
        '_id': id,
        'name': name,
        'email': email
    }

    with open(f'{file.filename}', 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)

    mongo = pymongo.MongoClient("localhost")
    db = mongo["tcc"]
    collection = db["test"]

    image = cv2.imread(file.filename)
    try:
        info["face_encoding"] = face_recognition.face_encodings(image)[
            0].tolist()
    except Exception as e:
        return {
            'error': f"Face not detected in file <{file}>",
            'msg': e
        }

    try:
        collection.insert_one(info)
    except Exception as e:
        return {"Error": e}

    mongo.close()

    return {
        '200': 'Upload successful'
    }

import os
from re import template
from urllib import request
import face_recognition
import cv2
import json
import pymongo
from fastapi import FastAPI, UploadFile, File, Form, Request, Body
from pydantic import BaseModel
import shutil
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


templates = Jinja2Templates(directory='template')

app = FastAPI()


@app.get('/', response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# @app.post('/test2', response_class=HTMLResponse)
# async def test(name: str = Form(...), ra: str = Form(...), email: str = Form(...), file: UploadFile = File(...)):
#     return '<h3>Enviado com Sucesso!</h3>'


@app.post('/test')
async def test(name: str = Form(...), ra: str = Form(...), email: str = Form(...), file: UploadFile = File(...)):
    info = {
        '_id': ra,
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
            'error': f"Face not detected in file <{file.filename}>",
            'msg': e
        }

    try:
        os.remove(file.filename)
    except:
        print(f"Falha ao remover o arquivo {file.filename}")

    try:
        collection.insert_one(info)
    except Exception as e:
        return {"Error": e}

    mongo.close()

    return {
        '200': 'Upload successful'
    }

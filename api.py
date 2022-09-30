import os
from re import template
import face_recognition
import cv2
import pymongo
from fastapi import FastAPI, UploadFile, File, Form, Request, Body
import shutil
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


templates = Jinja2Templates(directory='template')

app = FastAPI()

# Rota que contém o formulario
@app.get('/', response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Rota para envio dos dados para o banco
@app.post('/upload')
async def upload(name: str = Form(...), ra: str = Form(...), email: str = Form(...), file: UploadFile = File(...)):
    # Recebedo dados do formulario
    try:
        info = {
            '_id': ra,
            'name': name,
            'email': email
        }
    except Exception as e:
        return {
            'msg': e
        }

    # Recebendo a imagem
    with open(f'{file.filename}', 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Conexão com o banco
    mongo = pymongo.MongoClient("localhost")
    db = mongo["tcc"]
    collection = db["data"]

    # Ler a imagem
    image = cv2.imread(file.filename)
    # Criação dos encodings
    try:
        info["face_encoding"] = face_recognition.face_encodings(image)[
            0].tolist()
    except Exception as e:
        return {
            'error': f"Face not detected in file <{file.filename}>",
            'msg': e
        }

    # Remoção da imagem utilizada
    try:
        os.remove(file.filename)
    except:
        print(f"Falha ao remover o arquivo {file.filename}")

    # Enviando dados para o banco
    try:
        collection.insert_one(info)
    except Exception as e:
        return {"Error": e}

    # Encerrando conecão com o banco
    mongo.close()

    return {
        '200': 'Upload successful'
    }

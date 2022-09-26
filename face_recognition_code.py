import cv2
import numpy as np
import face_recognition
import pymongo

# Conexão ao banco de dados
mongo = pymongo.MongoClient("localhost")
db = mongo["tcc"]
collection = db["data"]
data = collection.find({})

known_faces_encodings = []
known_faces_ra = []

# Ler cada dado recebido do banco
for document in data:
    # Adicionar nome e id na lista
    first_name = str(document['name']).split(' ')[0]
    known_faces_ra.append(f"{first_name} : {document['_id']}")
    # Adicionar o encoding do rosto na lista
    known_faces_encodings.append(np.array(document["face_encoding"]))

# Encerrando conexão com o banco
mongo.close()

# Iniciar camera
capture = cv2.VideoCapture(0)

# Video
while True:
    # Ler as imagens
    ret, frame = capture.read()
    frame = cv2.flip(frame, 1)
    if ret:
        try:
            # Descobrir as localizações dos rostos no frame
            face_locations = face_recognition.face_locations(frame)
            frame_encoding = face_recognition.face_encodings(
                frame, face_locations)

            # Identificar todos os rostos no frame
            for (top, right, bottom, left), face_encoding in zip(face_locations, frame_encoding):
                # Comparar rosto no frame com os encodings do banco
                matches = face_recognition.compare_faces(
                    known_faces_encodings, face_encoding, tolerance=0.55)

                # Nome e cor padrão
                name = "Unkown"
                rect_color = (5, 5, 215)

                # Caso o rosto seja reconhecido
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_faces_ra[first_match_index]
                    rect_color = (5, 200, 5)

                # Desenhar um retângulo ao redor do rosto
                frame = cv2.rectangle(frame, (left, top),
                                      (right, bottom - 15), rect_color)
                # Desenhar um retângulo para colocar o nome
                frame = cv2.rectangle(
                    frame, (left, bottom), (right, bottom - 15), rect_color, -1)
                # Colocar o nome e id
                frame = cv2.putText(frame, name, (left + 2, bottom - 3),
                                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (255, 255, 255, 255))

            # Mostrar o frame
            cv2.imshow('Video', frame)
            if cv2.waitKey(5) == 27:
                break

        # Mostrar erro caso aconteça
        except Exception:
            print(Exception)

# Fechar o programa
capture.release()
cv2.destroyAllWindows()

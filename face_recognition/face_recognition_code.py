import cv2
import numpy as np
import face_recognition
import json
import pymongo

# Databse connection
mongo = pymongo.MongoClient("localhost")
db = mongo["tcc"]
collection = db["test"]
data = collection.find({})

known_faces_encodings = []
known_faces_ra = []

for document in data:
    first_name = str(document['name']).split(' ')[0]
    known_faces_ra.append(f"{first_name} : {document['_id']}")
    known_faces_encodings.append(np.array(document["face_encoding"]))
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
            # cv2.imshow('frame', frame)
            face_locations = face_recognition.face_locations(frame)
            print(face_locations)
            frame_encoding = face_recognition.face_encodings(
                frame, face_locations)

            found = []

            # Loop through faces in frame
            for (top, right, bottom, left), face_encoding in zip(face_locations, frame_encoding):
                matches = face_recognition.compare_faces(
                    known_faces_encodings, face_encoding, tolerance=0.55)

                # Defaut face name and color
                name = "Unkown"
                rect_color = (5, 5, 215)

                # If match found
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_faces_ra[first_match_index]
                    found.append(name)
                    rect_color = (5, 200, 5)

                # Draw rectangle arround the face
                frame = cv2.rectangle(frame, (left, top),
                                      (right, bottom - 15), rect_color)
                # Draw rectangle to put the name
                frame = cv2.rectangle(
                    frame, (left, bottom), (right, bottom - 15), rect_color, -1)
                # Draw the name and id
                frame = cv2.putText(frame, name, (left + 2, bottom - 3),
                                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (255, 255, 255, 255))

            print(found)

            # Display Image
            cv2.imshow('Video', frame)
            if cv2.waitKey(5) == 27:
                break

        # Show error if it ever happens
        except Exception:
            print(Exception)

# Fechar o programa
capture.release()
cv2.destroyAllWindows()

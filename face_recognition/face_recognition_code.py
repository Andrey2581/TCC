from cmath import pi
from turtle import right
import cv2
import numpy as np
import face_recognition
from PIL import Image, ImageDraw
import json

# Iniciar camera
capture = cv2.VideoCapture(0)
# capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
# capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

# my_photo = face_recognition.load_image_file(
#     'face_recognition\\images\\Nadson\\Nadson.jpg')
# my_photo = cv2.imread('./images/Nadson/Nadson.jpg')
# my_face_encoding = face_recognition.face_encodings(my_photo)[0]


with open('file_encoding.json', 'r') as file:
    encondings_from_json = json.load(file)

known_faces_encodings = []
known_faces_names = []

for key in encondings_from_json:
    for enconde in encondings_from_json[key]:
        known_faces_names.append(key)
        known_faces_encodings.append(np.array(enconde))

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

            # Convert to PIL format
            pil_image = Image.fromarray(frame)

            # Create a ImageDraw instance
            draw = ImageDraw.Draw(pil_image)

            found = []

            # Loop through faces in frame
            for (top, right, bottom, left), face_encoding in zip(face_locations, frame_encoding):
                matches = face_recognition.compare_faces(
                    known_faces_encodings, face_encoding, tolerance=0.55)

                # Defaut face name
                name = "Unkown Person"

                # If match
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_faces_names[first_match_index]
                    found.append(name)

                frame = cv2.rectangle(frame, (left, top),
                                      (right, bottom - 15), (5, 200, 5))
                frame = cv2.rectangle(
                    frame, (left, bottom), (right, bottom - 15), (5, 200, 5), -1)
                frame = cv2.putText(frame, name, (left + 2, bottom - 3),
                                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.6, (255, 255, 255, 255))

                # # Draw Box
                # draw.rectangle(((left, top), (right, bottom)),
                #                outline=(0, 0, 0))
                # # Draw Label
                # text_width, text_height = draw.textsize(name)
                # draw.rectangle(((left, bottom - text_height - 10),
                #                (right, bottom)), fill=(0, 0, 0), outline=(0, 0, 0))
                # draw.text((left + 6, bottom - text_height - 5),
                #           name, fill=(255, 255, 255, 255))

            # Delete ImageDraw instance
            del draw

            print(found)

            # Display Image
            cv2.imshow('Video', frame)
            # pil_image.show("Frame")
            if cv2.waitKey(5) == 27:
                break

        except Exception:
            # print(f'There are {len(face_locations)} people in this frame')
            print(Exception)
            # Mostrar o resultado
            # cv2.imshow('Video', frame)
            # Fechar o programa


capture.release()
cv2.destroyAllWindows()

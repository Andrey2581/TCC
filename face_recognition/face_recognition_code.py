import cv2
import numpy as np
import face_recognition
from PIL import Image, ImageDraw

# Iniciar camera
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

# my_photo = face_recognition.load_image_file('./images/Nadson.jpg')
my_photo = cv2.imread('./images/Nadson.jpg')
my_face_encoding = face_recognition.face_encodings(my_photo)[0]

# Video
while True:
    # Ler as imagens
    ret, frame = capture.read()
    frame = cv2.flip(frame, 1)

    # Tranformar em escala de cinza
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    try:
        face_locations = face_recognition.face_locations(frame)
        print(face_locations)
        top, right, bottom, left = face_locations[0]
        print('2')
        frame_encoding = face_recognition.face_encodings(
            frame)[0]
        print('3')

        results = face_recognition.compare_faces(
            [my_face_encoding], frame_encoding, tolerance=0.7)
        print('4')

        # pil_image = Image.fromarray(frame)
        # draw = ImageDraw.Draw(pil_image)

        # for (top, right, bottom, left), face_encoding in zip(face_locations, frame_encoding):
        #     results = face_recognition.compare_faces(
        #         [my_face_encoding], face_encoding)

        name = 'unknown'
        print(results)
        if True in results:
            name = 'Nadson'

        print('ok')
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 5), 3)
        cv2.putText(frame, name, (left, top),
                    cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, 255, 2)
        print('ok1')
        # draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 0))
        # text_width, text_height = draw.textsize(name)
        # draw.rectangle(((left, bottom - text_height - 10),
        #                 (right, bottom)), outline=(0, 0, 0), fill=(0, 0, 0))
        # draw.text((left + 6, bottom - text_height - 5),
        #           name, fill=(255, 255, 255, 255))

        # Mostrar o resultado
        cv2.imshow('Video0', frame)
        # Fechar o programa
        if cv2.waitKey(5) == 27:
            break

    except Exception:
        # print(f'There are {len(face_locations)} people in this frame')
        print(Exception)
        # Mostrar o resultado
        cv2.imshow('Video', frame)
        # Fechar o programa
        if cv2.waitKey(5) == 27:
            break

# del draw
capture.release()
cv2.destroyAllWindows()

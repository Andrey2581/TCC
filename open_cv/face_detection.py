import cv2
import numpy as np

# Iniciar camera
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

# Importar o classificador
faceCascade = cv2.CascadeClassifier(
    f'{cv2.data.haarcascades}haarcascade_frontalface_default.xml'
)

# Video
while True:
    # Ler as imagens
    ret, frame = capture.read()
    # Tranformar em escala de cinza
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Descobrir quantas faces tem na imagem
    faces = faceCascade.detectMultiScale(
        frame,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    # Colocar as posições e tamanhos dos rostos em listas
    face_size = []
    face_placement = []
    for (x, y, w, h) in faces:
        face_size.append(w.astype(int))
        face_placement.append((x, y, w, h))
    # Descobrir qual o maior rosto
    for i in range(5):
        try:
            index = face_size.index(max(face_size))
            face_size.pop(index)
            print(index)
            x, y, w, h = face_placement.pop(index)
            # Colocar um relangulo no maior rosto
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )
            # Escrever o tamanho do retangulo
            cv2.putText(frame, w.astype(str), (x + 10, y + 10),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, 255, 2)
        # Evitar erro caso nenhum rosto seja identificado
        except Exception as e:
            print(e)
            print(f'{i} faces found!')

    # Mostrar o resultado
    cv2.imshow('Video', frame)
    # Fechar o programa
    if cv2.waitKey(5) == 27:
        break

capture.release()
cv2.destroyAllWindows()

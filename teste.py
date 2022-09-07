import numpy as np
import cv2
import time

# matriz = np.array([
#     [[1, 1, 1], [1, 1, 1]],
#     [[2, 2, 2], [2, 2, 2]],
#     [[3, 3, 3], [3, 3, 3]],
# ])

# print(matriz[:, 1])

image = cv2.imread('face_recognition\\images\\Nadson\\Nadson.jpg')
print(image)
cv2.imshow('frame', image)
time.sleep(30)

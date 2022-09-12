import numpy as np
# import cv2
# import time

# # matriz = np.array([
# #     [[1, 1, 1], [1, 1, 1]],
# #     [[2, 2, 2], [2, 2, 2]],
# #     [[3, 3, 3], [3, 3, 3]],
# # ])

# # print(matriz[:, 1])

# image = cv2.imread('face_recognition\\images\\Nadson\\Nadson.jpg')
# print(image)
# cv2.imshow('frame', image)
# time.sleep(30)

import pymongo

mongo = pymongo.MongoClient("localhost")
db = mongo["tcc"]
collection = db["test"]

results = collection.find({})

for result in results:
    print(result.keys())

mongo.close()

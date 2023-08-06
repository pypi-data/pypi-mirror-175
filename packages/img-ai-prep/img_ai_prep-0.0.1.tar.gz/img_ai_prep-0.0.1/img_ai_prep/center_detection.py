from typing import Tuple

import cv2
import numpy as np
from PIL import Image


def face_center(img: Image.Image, **kwargs) -> Tuple[int, int]:
    if "model" in kwargs:
        model = kwargs["model"]
    else:
        model = cv2.CascadeClassifier(cv2.data.haarcascades +
                                      "haarcascade_frontalface_default.xml")

    if "scale_factor" in kwargs:
        scale_factor = kwargs["scale_factor"]
    else:
        scale_factor = 1.1

    if "min_neighbors" in kwargs:
        min_neighbors = kwargs["min_neighbors"]
    else:
        min_neighbors = 10

    if "min_size" in kwargs:
        min_size = kwargs["min_size"]
    else:
        size = int((img.size[0] + img.size[1]) / 2 * 0.10)
        min_size = (size, size)

    cv_img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
    faces = model.detectMultiScale(cv_img,
                                   scaleFactor=scale_factor,
                                   minNeighbors=min_neighbors,
                                   minSize=min_size)

    if (isinstance(faces, tuple) and len(faces) == 0) or (
            isinstance(faces, np.ndarray) and faces.shape[0] == 0):
        print("INFO: No face found, defaulting to center")
        return int(img.size[0] / 2), int(img.size[1] / 2)
    if faces.shape[0] == 1:
        return center_of_box(faces[0])
    else:
        overall_x = 0
        overall_y = 0
        for face in faces:
            center_of_face = center_of_box(face)
            overall_x += center_of_face[0]
            overall_y += center_of_face[1]
        avg_x = int(overall_x / faces.shape[0])
        avg_y = int(overall_y / faces.shape[0])
        return avg_x, avg_y


def center_of_box(box: Tuple[int, int, int, int]) -> Tuple[int, int]:
    """Box of x, y, width, height to center of box"""
    return box[0] + int(box[2] / 2), box[1] + int(box[3] / 2)

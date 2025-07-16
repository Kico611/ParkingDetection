import pickle
import os
from skimage.transform import resize
import numpy as np
import cv2

# Konstante za status mjesta
EMPTY = True
NOT_EMPTY = False

# Pronađi apsolutnu putanju do modela
this_dir = os.path.dirname(__file__)
model_path = os.path.join(this_dir, "model", "model.p")

# Učitaj model iz datoteke
MODEL = pickle.load(open(model_path, "rb"))

# Funkcija koja provjerava je li parking mjesto prazno
def empty_or_not(spot_bgr):
    flat_data = []
    img_resized = resize(spot_bgr, (15, 15, 3))
    flat_data.append(img_resized.flatten())
    flat_data = np.array(flat_data)
    y_output = MODEL.predict(flat_data)

    return EMPTY if y_output == 0 else NOT_EMPTY

# Funkcija koja iz connected components izvlači koordinate parking mjesta
def get_parking_spots_bboxes(connected_components):
    (totalLabels, label_ids, values, centroid) = connected_components
    slots = []
    coef = 1
    for i in range(1, totalLabels):
        x1 = int(values[i, cv2.CC_STAT_LEFT] * coef)
        y1 = int(values[i, cv2.CC_STAT_TOP] * coef)
        w = int(values[i, cv2.CC_STAT_WIDTH] * coef)
        h = int(values[i, cv2.CC_STAT_HEIGHT] * coef)
        slots.append([x1, y1, w, h])
    return slots


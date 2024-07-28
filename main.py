# pip install pyzbar
import os

import cv2
import matplotlib.pyplot as plt
import numpy as np
from pyzbar.pyzbar import  decode
input_dir = "./data"

for j in os.listdir(input_dir):
    img = cv2.imread(os.path.join(input_dir,j))
    qr_info = decode(img)
    print(qr_info)
    for qr in qr_info:
        data = qr.data
        rect = qr.rect
        polygon = qr.polygon

        print(data)
        print(rect)
        print(polygon)
        print()

        img = cv2.rectangle(img, (rect.left, rect.top), (rect.left + rect.width, rect.top + rect.height), (0,255,0), 10)

        img = cv2.polylines(img, [np.array(polygon)], True, (255,0,0), 10   )

        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.show()
    # cv2.imshow('img',img)

# cv2.waitKey(0)


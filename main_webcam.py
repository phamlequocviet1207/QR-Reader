import datetime
from pyzbar.pyzbar import decode
import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime
import time
import math

cap = cv2.VideoCapture(0)

authorized_users = []
with open ('./authorized_users.txt', 'r') as file:
    for line in file:
        line = line.strip("\n")
        authorized_users.append(line)
    file.close()
# print(authorized_users)

log_path = "./log.txt"

most_recent_access = {}

time_between_log = 10

while True:
    ret, frame = cap.read()
    qr_info = decode(frame)
    if len(qr_info) > 0:
        # print(qr_info)
        qr = qr_info[0]

        data = qr.data
        rect = qr.rect
        polygon = qr.polygon

        if data.decode() in authorized_users:
            now = datetime.now()
            cv2.putText(frame, "ACCESS GRANTED", (rect.left, rect.top - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
            # print(time.time())
            # print("now",now)
            if data.decode() not in most_recent_access.keys() \
                    or time.time() - most_recent_access[data.decode()] > time_between_log:

                most_recent_access[data.decode()] = time.time()

                with open(log_path, 'a') as file:

                    file.write('{}, {}\n'.format(data.decode(), now))
                    file.close()
        else:
            cv2.putText(frame, "ACCESS DENIED", (rect.left, rect.top - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255),
                        2)
        # print(type(data))
        # cv2.putText(frame, data.decode(), (rect.left, rect.top-30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)

        frame = cv2.rectangle(frame, (rect.left, rect.top), (rect.left + rect.width, rect.top + rect.height), (0,255,0), 10)

        frame = cv2.polylines(frame, [np.array(polygon)], True, (255,0,0), 10)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()

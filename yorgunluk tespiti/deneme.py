from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2
import os
from datetime import datetime

def lip_distance(shape):
    top_lip = shape[50:53]
    top_lip = np.concatenate((top_lip, shape[61:64]))

    low_lip = shape[56:59]
    low_lip = np.concatenate((low_lip, shape[65:68]))

    top_mean = np.mean(top_lip, axis=0)
    low_mean = np.mean(low_lip, axis=0)

    distance = abs(top_mean[1] - low_mean[1])
    return distance

YAWN_THRESH = 25
i=0
esneme_sayisi=0

ap = argparse.ArgumentParser()
ap.add_argument("-w", "--webcam", type=int, default=0,
                help="index of webcam on system")
args = vars(ap.parse_args())

vs = VideoStream(src=args["webcam"]).start()

detector = cv2.CascadeClassifier("models/haarcascade_frontalface_default.xml")    #Faster but less accurate
predictor = dlib.shape_predictor('models/shape_predictor_68_face_landmarks.dat')

while True:

    frame = vs.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #rects = detector.detectMultiScale(gray, 0)
    rects = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.CASCADE_SCALE_IMAGE)

    for (x, y, w, h) in rects:
        rect = dlib.rectangle(int(x), int(y), int(x + w), int(y + h))

        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        distance = lip_distance(shape)

        lip = shape[48:60]
        cv2.drawContours(frame, [lip], -1, (0, 255, 0), 1)
        if (distance > YAWN_THRESH):
            i+=1
            print(i)
            if(i%20==0):
                esneme_sayisi+=1
            cv2.putText(frame, "Yawn Alert", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

cv2.destroyAllWindows()
vs.stop()
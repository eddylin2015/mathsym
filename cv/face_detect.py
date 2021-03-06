import cv2
import numpy as np
import time
import sys

cap=cv2.VideoCapture(0)
while(cap.isOpened()):
    ret,frame=cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=3,
        minSize=(30, 30)
    )
    
    print("[INFO] Found {0} Faces!".format(len(faces)))
    
    
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('Frame',frame)

    if cv2.waitKey(1)&0xff==ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
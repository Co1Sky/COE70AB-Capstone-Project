#!/usr/bin/python3

import cv2
import time

from picamera2 import Picamera2
from libcamera import Transform

# Grab images as numpy arrays and leave everything else to OpenCV.

def start_face_detect():
    face_detector = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")
    cv2.startWindowThread()

    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)},
    transform = Transform(vflip=1,hflip=1)))
    picam2.start()

    start_time = time.time()
    frame_count = 0

    while True:
        im = picam2.capture_array()

        grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(grey, 1.1, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0))

        cv2.putText(im, f"FPS: {frame_count / (time.time() - start_time):.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        frame_count += 1

        cv2.imshow("Camera", im)
        cv2.waitKey(1)

#start_face_detect()


import time

import cv2
from picamera2 import Picamera2, Preview
from libcamera import Transform

face_detector = cv2.CascadeClassifier("/home/student/picamera2-examples/examples/haarcascade_frontalface_default.xml")

preview_type = Preview.QTGL

print("First preview...")
Picamera2.set_logging()
picam2 = Picamera2()
preview_config = picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (320, 240)},
                                                     transform = Transform(vflip=1))
picam2.configure(preview_config)
picam2.start()
time.sleep(2)
while True:
    im = picam2.capture_array()

    grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(grey, 1.1, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0))

    cv2.imshow("Facial Recognition is Running", im)
    key = cv2.waitKey(1) & 0xFF

    # quit when 'q' key is pressed
    if key == ord("q"):
        break
    
cv2.destroyAllWindows()
picam2.close()
print("Done")

print("Second preview...")
picam2 = Picamera2()
preview_config = picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (320, 240)},
                                                     transform = Transform(vflip=1))
picam2.configure(preview_config)
picam2.start()
time.sleep(2)
while True:
    im = picam2.capture_array()

    grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(grey, 1.1, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0))

    cv2.imshow("Facial Recognition is Running", im)
    key = cv2.waitKey(1) & 0xFF

    # quit when 'q' key is pressed
    if key == ord("q"):
        break
cv2.destroyAllWindows()
picam2.close()
print("Done")
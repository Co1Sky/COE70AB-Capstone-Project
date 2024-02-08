import cv2
import dlib
import math
import numpy as np
from cv2 import FONT_HERSHEY_COMPLEX_SMALL

# Load the pre-trained face detector and facial landmarks predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Initialize the webcam
cap = cv2.VideoCapture(0)

while True:
    # Read the frame from the webcam
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces using the dlib face detector
    faces = detector(gray)

    for face in faces:
        # Get facial landmarks
        shape = predictor(gray, face)

        # Draw a rectangle around the face detected by OpenCV
        x, y, w, h = face.left(), face.top(), face.width(), face.height()
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        mid_x = int(x+w/2)
        mid_y = int(y+h/2)
        nose_tip = shape.part(30)
        nose_top = shape.part(27)

        cv2.line(frame, (mid_x, y), (mid_x, y + h), (255, 0, 0), 1)
        cv2.line(frame, (x, nose_tip.y), (x+w, nose_tip.y), (255, 0, 0), 1)
        cv2.line(frame, (nose_top.x, nose_top.y), (nose_tip.x, nose_tip.y), (0, 255, 0), 2)

        vectorA = np.array([[nose_top.x, nose_top.y], [nose_tip.x, nose_tip.y]])
        vectorB = np.array([[mid_x, y], [mid_x, nose_tip.y]])
        distVectorA = vectorA[1] - vectorA[0]
        distVectorB = vectorB[1] - vectorB[0]
        dot_product = np.dot(distVectorA, distVectorB)
        norm_vectorA = np.linalg.norm(distVectorA)
        norm_vectorB = np.linalg.norm(distVectorB)
        cosine = dot_product / (norm_vectorA * norm_vectorB)
        angle = np.arccos(cosine)
        angle = round(np.degrees(angle))
        cv2.putText(frame, str(angle), (mid_x, y-10), FONT_HERSHEY_COMPLEX_SMALL, 1.25, (0, 0, 255), 1)
        cv2.putText(frame, str(distVectorA[1]), (mid_x, y - 30), FONT_HERSHEY_COMPLEX_SMALL, 1.25, (0, 0, 255), 1)

    # Display the frame
    cv2.imshow('Head Tilt Detection', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

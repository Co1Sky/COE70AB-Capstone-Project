import sys
import cv2
import dlib
import imutils
import time
import math
import numpy as np
from cv2 import FONT_HERSHEY_COMPLEX_SMALL
from picamera2 import Picamera2, Preview
from libcamera import Transform
from datetime import datetime
from parameters import *
from scipy.spatial import distance
from imutils import face_utils as person_face

sys.path.append("Drowsiness Detection Code/")
sys.path.append("Servo Scan Code/")
sys.path.append("Face Recognition Code/")

# Function to zoom in by adjusting the crop region
def zoom_in():
    size = picam2.capture_metadata()['ScalerCrop'][2:]
    full_res = picam2.camera_properties['PixelArraySize']
    picam2.capture_metadata()
    size = [int(s * 0.85) for s in size]
    offset = [(r - s) // 2 for r, s in zip(full_res, size)]
    picam2.set_controls({"ScalerCrop": offset + size})


# Function to zoom out by adjusting the crop region
def zoom_out():
    size = picam2.capture_metadata()['ScalerCrop'][2:]
    full_res = picam2.camera_properties['PixelArraySize']
    picam2.capture_metadata()
    size = [int(s / 0.85) for s in size]
    offset = [(r - s) // 2 for r, s in zip(full_res, size)]
    picam2.set_controls({"ScalerCrop": offset + size})
    
def convert_point(x, y, x_offset, y_offset, original_width, original_height, new_width, new_height):
    # Calculate the scaling factors for x and y coordinates
    x_scale = new_width / original_width
    y_scale = new_height / original_height
    
    # Apply the scaling factors to the original coordinates
    new_x = int(x * x_scale)
    new_y = int(y * y_scale)
    new_x_offset = int(x_offset * x_scale)
    new_y_offset = int(y_offset * y_scale)
    return new_x, new_y, new_x_offset, new_y_offset

#draw a bounding box over face
def get_max_area_rect(rects):
    # checks to see if a face was not dectected (0)
    if len(rects)==0: return
    areas=[]
    for rect in rects:
        areas.append(rect.area())
    return rects[areas.index(max(areas))]

#computes the mouth aspect ratio (mar)
def get_mouth_aspect_ratio(mouth):
    # mouth landmarks (x, y)-coordinates
    horizontal=distance.euclidean(mouth[0],mouth[4])
    vertical=0
    for coord in range(1,4):
        vertical+=distance.euclidean(mouth[coord],mouth[8-coord])
    #return MAR
    return vertical/(horizontal*3)

#computes the eye aspect ratio (ear)
def get_eye_aspect_ratio(eye):
    # eye landmarks (x, y)-coordinates
    vertical_1 = distance.euclidean(eye[1], eye[5])
    vertical_2 = distance.euclidean(eye[2], eye[4])
    horizontal = distance.euclidean(eye[0], eye[3])
    #returns EAR
    return (vertical_1+vertical_2)/(horizontal*2)

def facial_processing(faceCoordinates,num_people):
    distracton_initialized = False
    eye_initialized      = False
    mouth_initialized    = False
    normal_initialized   = False
    
    screenWidth = 800
    screenHeight = 600

    detector = dlib.get_frontal_face_detector()
    predictor   = dlib.shape_predictor('/home/student/mcr4-version-3.0/shape_predictor_68_face_landmarks.dat')
    
    ls,le = person_face.FACIAL_LANDMARKS_IDXS["left_eye"]
    rs,re = person_face.FACIAL_LANDMARKS_IDXS["right_eye"]

    print("-->  Starting Video Stream")
    picam2 = Picamera2()
    preview_config = picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (screenWidth, screenHeight)},
                                                         transform = Transform(vflip=1))
    picam2.configure(preview_config)
    picam2.start()
    
    while True:
        frame = picam2.capture_array()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        face = get_max_area_rect(faces)
        
        if face!=None:
            num_people.value = 1
            
            center_x = ((face.left() + face.right()) // 2)
            center_y = ((face.top() + face.bottom()) // 2)
            faceCoordinates[0] = int(center_x - screenWidth / 2)
            faceCoordinates[1] = int(screenHeight /2 - center_y)
            print(f"{faceCoordinates[0]}:{faceCoordinates[1]}")
            
            #measures the duration the users eyes were off the road
            if distracton_initialized==True:
                interval=time.time()-distracton_start_time
                interval=str(round(interval,3))
                #gets the current date/time
                dateTime= datetime.now()
                distracton_initialized=False
                info="Date: " + str(dateTime) + ", Interval: " + interval + ", Type: Eyes not on road"
                info=info+ "\n"
                if time.time()- distracton_start_time> DISTRACTION_INTERVAL:
                    #stores the info into a txt file
                    with open(r'/home/student/mcr4-version-3.0/output.txt', "a+") as file_object:
                        file_object.write(info)
            
            # Get facial landmarks
            shape = predictor(gray, face)
            dlib_face = person_face.shape_to_np(shape)

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
            
            x,y,w,h = convert_point(x,y,w,h,screenWidth,screenHeight,2592,1944)

            # extract the left and right eye coordinates, then use the
            # coordinates to compute the eye aspect ratio for both eyes
            leftEye = dlib_face[ls:le]
            rightEye = dlib_face[rs:re]
            #gets the EAR for each eye
            leftEAR = get_eye_aspect_ratio(leftEye)
            rightEAR = get_eye_aspect_ratio(rightEye)

            inner_lips=dlib_face[60:68]
            mar=get_mouth_aspect_ratio(inner_lips)

            # average the eye aspect ratio together for both eyes
            eye_aspect_ratio = (leftEAR + rightEAR) / 2.0

            # compute the convex hull for the left and right eye, then
            # visualize each of the eyes, draw bounding boxes around eyes
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(frame, [leftEyeHull], -1, (255, 255, 255), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (255, 255, 255), 1)
            lipHull = cv2.convexHull(inner_lips)
            cv2.drawContours(frame, [lipHull], -1, (255, 255, 255), 1)

            #display EAR on screen
            cv2.putText(frame, "EAR: {:.2f} MAR{:.2f}".format(eye_aspect_ratio,mar), (10, frame.shape[0]-10),\
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            #checking if eyes are drooping/almost closed
            if eye_aspect_ratio < EYE_DROWSINESS_THRESHOLD:

                if not eye_initialized:
                    eye_start_time= time.time()
                    eye_initialized=True
                #checking if eyes are drowsy for a sufficient number of frames
                if time.time()-eye_start_time >= EYE_DROWSINESS_INTERVAL:
                    cv2.putText(frame, "YOU ARE DROWSY!", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    #uncomment the three lines below to help check the validity of the program
                    #dateTimeOBJ=datetime.now()
                    #eye_info="Date: " + str(dateTimeOBJ) + " Interval: " + str(time.time()-eye_start_time ) + " Drowsy"
                    #print(eye_info)

            else:
                #measures the duration where the users eyes were drowsy
                if eye_initialized==True:
                    interval_eye=time.time()-eye_start_time
                    interval_eye=str(round(interval_eye,3))
                    dateTime_eye= datetime.now()
                    eye_initialized=False
                    info_eye="Date: " + str(dateTime_eye) + ", Interval: " + interval_eye + ", Type:Drowsy"
                    info_eye=info_eye+ "\n"
                    ##will only store the info if user eyes close/droop for a sufficient amount of time
                    if time.time()-eye_start_time >= EYE_DROWSINESS_INTERVAL:
                    #store info into a txt file
                        with open(r'/home/student/mcr4-version-3.0/output.txt', "a+") as file_object:
                            file_object.write(info_eye)



            #checks if user is yawning
            if mar > MOUTH_DROWSINESS_THRESHOLD:

                if not mouth_initialized:
                    mouth_start_time= time.time()
                    mouth_initialized=True
                #checks if the user is yawning for a sufficient number of frames
                if time.time()-mouth_start_time >= MOUTH_DROWSINESS_INTERVAL:
                    cv2.putText(frame, "YOU ARE YAWNING!", (10, 70),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    #uncomment the lines below to check the validity of this program
                    #dateTimeOBJ2=datetime.now()
                    #mouth_info="date: " + str(dateTimeOBJ2) + " Interval: " + str(time.time()-mouth_start_time ) + " Yawning" + " mar " + str(mar)
                    #print(mouth_info)

            else:
                #measures duration of users yawn
                if mouth_initialized==True:
                    interval_mouth=time.time()-mouth_start_time
                    interval_mouth=str(round(interval_mouth,3))
                    dateTime_mouth= datetime.now()
                    mouth_initialized=False
                    info_mouth="Date: " + str(dateTime_mouth) + ", Interval: " + interval_mouth + ", Type:Yawning"
                    info_mouth=info_mouth+ "\n"
                    #will only store the info if user yawns for a sufficient amount of time
                    if time.time()-mouth_start_time >= MOUTH_DROWSINESS_INTERVAL:
                    #store into into a txt file
                        with open(r'/home/student/mcr4-version-3.0/output.txt', "a+") as file_object:
                            file_object.write(info_mouth)


            #checks if the user is focused
            if (eye_initialized==False) & (mouth_initialized==False) & (distracton_initialized==False):

                if not normal_initialized:
                    normal_start_time= time.time()
                    normal_initialized=True

                #checks if the user is focused for a sufficient number of frames
                if time.time()-normal_start_time >= NORMAL_INTERVAL:
                        cv2.putText(frame, "Normal!", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        #print('Normal')
            else:
                if normal_initialized==True:
                    interval_normal=time.time()-normal_start_time
                    interval_normal=str(round(interval_normal,3))
                    dateTime_normal= datetime.now()
                    normal_initialized=False
                    info_normal="Date: " + str(dateTime_normal) + ", Interval: " + interval_normal+ ", Type:Normal"
                    info_normal=info_normal+ "\n"
                    #will only store the info if user is focused for a sufficient amount of time
                    if time.time()-normal_start_time >= NORMAL_INTERVAL:
                        with open(r'/home/student/mcr4-version-3.0/output.txt', "a+") as file_object:
                            file_object.write(info_normal)
                            
        else:
            num_people.value = 0

            if eye_initialized==True:
                    interval_eye=time.time()-eye_start_time
                    interval_eye=str(round(interval_eye,3))
                    dateTime_eye= datetime.now()
                    eye_initialized=False
                    info_eye="Date: " + str(dateTime_eye) + ", Interval: " + interval_eye + ", Type:Drowsy"
                    info_eye=info_eye+ "\n"
                    if time.time()-eye_start_time >= EYE_DROWSINESS_INTERVAL:
                        with open(r'/home/student/mcr4-version-3.0/output.txt', "a+") as file_object:
                            file_object.write(info_eye)

            if not distracton_initialized:
                distracton_start_time=time.time()
                distracton_initialized=True
                #eye_initialized=False
            #checks if the user's eyes are off the road after a sufficient number of frames
            if time.time()- distracton_start_time> DISTRACTION_INTERVAL:
                #displays on screen that the driver's eyes are off the road
                cv2.putText(frame, "PLEASE KEEP EYES ON ROAD", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                #uncomment the line below if want to check the validity of the program
                #dateTimeOBJ3=datetime.now()
                #DIST_info="date: " + str(dateTimeOBJ3) + " Interval: " + str(time.time()-distracton_start_time) + " EYES NOT ON ROAD"
                #print(DIST_info)

        # Full image size: (2592, 1944) 

        # Display the frame
        cv2.imshow('Head Tilt Detection', frame)


        # Check for keyboard input to control zooming
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('i'):  # Zoom in
            picam2.set_controls({"ScalerCrop": [x, y, w, h]})
        elif key == ord('o'):  # Zoom out
            x,y,w,h = convert_point(0,0,800,600,screenWidth,screenHeight,2592,1944)
            picam2.set_controls({"ScalerCrop": [x,y,w,h]})

    # Release the webcam and close all OpenCV windows
    cv2.destroyAllWindows()
    picam2.close()


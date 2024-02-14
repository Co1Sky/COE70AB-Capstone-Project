# Global Imports
import sys
import time
import multiprocessing
from multiprocessing import Value
from picamera2 import Picamera2
from libcamera import Transform
import pandas as pd

sys.path.append("Drowsiness Detection Code/")
sys.path.append("Servo Scan Code/")
sys.path.append("Face Recognition Code/")

# File Imports
from drowsiness import facial_processing
import servo_scan as ss
from servo_scan import start_servo
from usr_login import run_login
    
if __name__ =='__main__':
    
    print("--> Initializing the Servo Setting....")
    # SERVO MOTOR SETTINGS - DO NOT CHANGE!! #
    pan = ss.Servo(pin=13, max_angle=60, min_angle=-60)
    tilt = ss.Servo(pin=12, max_angle=30, min_angle=-70)
    
    print("--> Resetting the Camera & Servo Processes")
    pan_resetAngle = 0
    tilt_resetAngle = -20
    pan.set_angle(pan_resetAngle)
    tilt.set_angle(tilt_resetAngle)
    time.sleep(1.5)
    
    firstName, lastName = run_login()
    
    print("--> Initializing the Camera & Servo Processes")
    userData = pd.read_csv('Face Recognition Code/User Database/Current User Names.txt', delimiter=',')
    auth_user = userData[(userData['First Name'] == firstName) & (userData['Last Name'] == lastName)]
    print(auth_user['Pan Angle'].values[0])
    print(auth_user['Tilt Angle'].values[0])
    pan_initializeAngle = auth_user['Pan Angle'].values[0]
    tilt_initializeAngle = auth_user['Tilt Angle'].values[0]
    pan.set_angle(pan_initializeAngle)
    tilt.set_angle(tilt_initializeAngle)
    time.sleep(1.5)
        
    # VARIABLES SHARED BETWEEN THE TWO RUNNING PROCESSES
    faceCoordinates = multiprocessing.Array('i', 2)
    num_people = multiprocessing.Value('i', 0)
    
    # SETTING UP MULTIPROCESSING TASK 
    print("--> Starting Camera")
    camera_task = multiprocessing.Process(target=facial_processing,args=(faceCoordinates,num_people,))
    camera_task.start()
    time.sleep(5)
    
    print("--> Starting Servos")
    servo_task = multiprocessing.Process(target=start_servo, args=(firstName,lastName,pan,tilt,num_people,faceCoordinates))
    servo_task.start()
    time.sleep(1)
        
    


# Global Imports
import time
import multiprocessing
# File Imports
import drowsiness_detect as dd
import servo_scan as ss
import opencv_face_detect as opencv
    
if __name__ =='__main__': 
    print("--> Initializing the Servo Setting....")
    # SERVO MOTOR SETTINGS - DO NOT CHANGE!! #
    pan = ss.Servo(pin=13, max_angle=60, min_angle=-60)
    tilt = ss.Servo(pin=12, max_angle=30, min_angle=-70)
    panAngle = 0
    tiltAngle = -20
    pan.set_angle(panAngle)
    tilt.set_angle(tiltAngle)
    time.sleep(1)
    print("--> Initializing the Camera & Servo Processes")
    time.sleep(1)
    
    # SETTING UP MULTIPROCESSING TASK #
    # ------- Harsanjam's Drowsiness Detection Code ------- #
    camera_task = multiprocessing.Process(target=dd.start_drowsiness_detect)
    
    # ------- Basic OpenCV Face Detect ------#
    #camera_task2 = multiprocessing.Process(target=opencv.start_face_detect)
    
    # ------- Servo Task ------- #
    servo_task = multiprocessing.Process(target=ss.searching, args=(pan,tilt))
    
    print("--> Starting Camera")
    camera_task.start()
    #camera_task2.start()
    time.sleep(5)
    
    print("--> Starting Servo")
    #servo_task.start()
    
    


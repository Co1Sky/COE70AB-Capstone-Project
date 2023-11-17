# Global Imports
import time
import multiprocessing
from multiprocessing import Value

# File Imports
from drowsiness import facial_processing
import servo_scan as ss
from servo_scan import start_servo

    
if __name__ =='__main__': 
    print("--> Initializing the Servo Setting....")
    # SERVO MOTOR SETTINGS - DO NOT CHANGE!! #
    pan = ss.Servo(pin=13, max_angle=60, min_angle=-60)
    tilt = ss.Servo(pin=12, max_angle=30, min_angle=-70)
    
    print("--> Resetting the Camera & Servo Processes")
    pan_resetAngle = 0
    tilt_resetAngle = 0
    pan.set_angle(pan_resetAngle)
    tilt.set_angle(tilt_resetAngle)
    time.sleep(1.5)
       
    print("--> Initializing the Camera & Servo Processes")
    pan_initializeAngle = 60
    tilt_initializeAngle = 20
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
    servo_task = multiprocessing.Process(target=start_servo, args=(pan,tilt,num_people,faceCoordinates))
    servo_task.start()
    time.sleep(1)
        
    
    
    


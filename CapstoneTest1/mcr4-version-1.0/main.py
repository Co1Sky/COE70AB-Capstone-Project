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
    panAngle = 0
    tiltAngle = -20
    pan.set_angle(panAngle)
    tilt.set_angle(tiltAngle)
    time.sleep(1)
    print("--> Initializing the Camera & Servo Processes")
    time.sleep(1)
    
    #VARIABLES
    faceCoordinates = multiprocessing.Array('i', 2)
    num_people = multiprocessing.Value('i', 0)
    
    # SETTING UP MULTIPROCESSING TASK #
    print("--> Starting Camera")
    camera_task = multiprocessing.Process(target=facial_processing,args=(faceCoordinates,num_people,))
    camera_task.start()
    time.sleep(5)
    
    print("--> Starting Servos")
    servo_task = multiprocessing.Process(target=start_servo, args=(pan,tilt,num_people,faceCoordinates))
    servo_task.start()
    time.sleep(1)
        
    # while True:
        # # Access the coordinates from camera_task process
        # x, y = faceCoordinates[0], faceCoordinates[1]
        # print("[In main.py] Coordinates:", x, y)
        
        # # Access the number of people from the camera_task process
        # print("[In main.py] The Number of People: ",num_people.value)
        # time.sleep(1)
        
    
    
    


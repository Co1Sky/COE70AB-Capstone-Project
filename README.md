# COE70AB-Capstone-Project
This is a Github Repository for my Capstone Project at Toronto Metropolitan University. This will be used to store the current Python code for the project and where any new changes will be made. The list of dependencies below will be updated as the project moves forward. <br /> <br />

## Python Virtual Environment "virtualenv" <br />
The Capstone project is created in a Python Virtual Environment with the use of the **virtualenv** library. For more information on that library head to https://virtualenv.pypa.io/en/latest/. <br /> <br />

## Picamera2 Library <br />
As the RaspberryPi is using a 64bit OS, the original **picamera** library is unusable which is why we are now using the updated (**beta version**) **picamera2** library which is able to work on 64bit systems. For more information head to the following links below: <br />
- **Github Page**: https://github.com/raspberrypi/picamera2
- **Manual**: https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf

## Current Python Dependencies
### Tested
**Works with the following scripts: <br /> 
"Camera_Test.py" <br /> 
"Servo_Scan_Test.py" <br /> 
"Camera_Servo.py"** <br />
- picamera2  (Version: 0.3.12)
- pigpio     (Version 1.78)
- numpy      (Version 1.26.1)
- scipy      (Version 1.11.3)
- libcamera  (Built-in with RaspberryPi)

### Un-Tested
- opencv-python  (Version 4.8.1.78)
- dlib           (Version 19.24.2)

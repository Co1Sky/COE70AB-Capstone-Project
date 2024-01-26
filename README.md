# COE70AB-Capstone-Project
This is a Github Repository for my Capstone Project at Toronto Metropolitan University. This will be used to store the current Python code for the project and where any new changes will be made. The list of dependencies below will be updated as the project moves forward. <br /> <br />

## Python Virtual Environment "virtualenv"
The Capstone project is created in a Python Virtual Environment with the use of the **virtualenv** library. For more information on that library head to https://virtualenv.pypa.io/en/latest/. <br /> <br />

## Picamera2 Library
As the RaspberryPi is using a 64bit OS, the original **picamera** library is unusable which is why we are now using the updated (**beta version**) **picamera2** library which is able to work on 64bit systems. For more information head to the following links below: <br />
- **Github Page**: https://github.com/raspberrypi/picamera2
- **Manual**: https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf

## Project Task Check-List
- [x] Get Picamera working with the **picamera2** library
- [x] Get the servo motors working with the **pigpio** library
- [x] Picamera + Servo
- [x] Implement Harsanjam's Drowsiness Detection Code with **OpenCV-Python** & **Dilib**
- [x] Harsanjam's Drowsiness Detection Code + Servo scan function
- [x] Getting Raspberry Pi to control an LED
- [x] Drowsiness + Servo + LED 

## Current Python Dependencies
### Tested
- picamera2  (Version: 0.3.12)
- pigpio     (Version 1.78)
- numpy      (Version 1.26.1)
- scipy      (Version 1.11.3)
- libcamera  (Built-in with RaspberryPi)
- imutils    (Version 0.5.4)
- dlib       (Version 19.24.2)
- python3-opencv (Version 4.5.1+dfsg-5) **(Installed using apt-get rather than pip3)**
  
### Un-Tested

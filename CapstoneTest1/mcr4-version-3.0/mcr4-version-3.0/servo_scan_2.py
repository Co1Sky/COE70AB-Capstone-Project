import pigpio
from time import sleep
# Start the pigpiod daemon
import subprocess
result = None
status = 1
offset = 0
for x in range(3):
    p = subprocess.Popen('sudo pigpiod', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = p.stdout.read().decode('utf-8')
    status = p.poll()
    if status == 0:
        break
    sleep(0.2)
if status != 0:
    print(status, result)
'''
> Use the DMA PWM of the pigpio library to drive the servo
> Map the servo angle (0 ~ 180 degree) to (-90 ~ 90 degree)
'''

class Servo():
    MAX_PW = 1250  # 0.5/20*100
    MIN_PW = 250 # 2.5/20*100
    _freq = 50 # 50 Hz, 20ms
 
    def __init__(self, pin, min_angle=-90, max_angle=90):

        self.pi = pigpio.pi()
        self.pin = pin 
        self.pi.set_PWM_frequency(self.pin, self._freq)
        self.pi.set_PWM_range(self.pin, 10000)      
        self.angle = 0
        self.max_angle = max_angle
        self.min_angle = min_angle
        self.pi.set_PWM_dutycycle(self.pin, 0)

    def set_angle(self, angle):
        if angle > self.max_angle:
            angle = self.max_angle
        elif angle < self.min_angle:
            angle = self.min_angle
        self.angle = angle
        duty = self.map(angle, -90, 90, 250, 1250)
        self.pi.set_PWM_dutycycle(self.pin, duty)


    def get_angle(self):
        return self.angle

    # will be called automatically when the object is deleted
    # def __del__(self):
    #     pass

    def map(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

#---------------------------------------------------------------------------------
# End of servo class
#---------------------------------------------------------------------------------

def start_servo(pan, tilt, num_people, faceCoordinates):
    # start_servo() BODY
    x_block = 0   
    y_level = 0
    if(num_people.value == 1):
        found_face(x_block, y_level)
    else:
        searching(x_block, y_level) 



    
        


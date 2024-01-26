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
  

def start_servo(pan, tilt, num_people, faceCoordinates):
    def searching():
        while (num_people.value == 0):
            x_angle = 60
            y_angle = 20
            counter  = 0
            if(y_angle == 20):
                for y_val in range(20,-61,-10):
                    counter = counter + 1
                    y_angle = y_val
                    print("LEVEL{0}  -  Y angle: {1}".format(counter, y_angle))
                    print("------------------------")
                    if (x_angle == 60):
                        for x_val in range(60,-61,-2):
                            x_angle = x_val
                            pan.set_angle(x_angle)    
                            tilt.set_angle(y_angle) 
                            #print("X angle: ", x_angle)
                            if(num_people.value == 1):
                                found_face()
                            sleep(0.09)
                    elif (x_angle == -60):
                        print
                        for x_val in range(-60,61,2):
                            pan.set_angle(x_val)    
                            tilt.set_angle(y_val)
                            x_angle = x_val
                            #print("X angle: ", x_angle)
                            if(num_people.value == 1):
                                found_face()
                            sleep(0.09)
                    print("")
            elif (y_angle == -40):
                exit(0)
                
    def found_face():
        print("I HAVE FOUND A PERSON!!!!! YAY!!")
        sleep(5)
        while(True):
            delta_x = faceCoordinates[0]
            delta_y = faceCoordinates[1]
            print(f"x:{delta_x}, y:{delta_y}")
            def move_x():
                if (delta_x < -50):
                    new_angle = pan.get_angle() + 2
                    pan.set_angle(new_angle)
                elif (delta_x > 100):
                    new_angle = pan.get_angle() - 2
                    pan.set_angle(new_angle)
            def move_y():
                if (delta_y < -50):
                    new_angle = tilt.get_angle() + 2
                    tilt.set_angle(new_angle)
                elif (delta_y > 50):
                    new_angle = tilt.get_angle() - 2
                    tilt.set_angle(new_angle)
            sleep(0.5)
            move_x()
            move_y()
            #print(delta_x, delta_y)
            if(num_people.value == 0):
                # fail safe if it was a false positive that the face was lost
                sleep(5)
                if(num_people.value == 0):
                    searching()
            
    if(num_people.value == 1):
        found_face()
    else:
        searching()            
    
            
    
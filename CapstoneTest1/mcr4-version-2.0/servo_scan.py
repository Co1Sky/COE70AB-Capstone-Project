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

    def map(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def start_servo(pan, tilt, num_people, faceCoordinates):
    # 1st method -->> searching(int x_block, int y_level)
    def searching(x_block, y_level):
        while num_people.value == 0:

            # CASE1 - Traversing from the initial to end point till a human face
            # is detected. This occurs ONLY when either of the following
            # cases take place:
            # 1st >> 'searching()' was just called by 'start_servo()'
            # 2nd >> traversed through the entire camera's surrounding
            # but no human faces were detected
            # 3rd >> detected a human face at level1 OR 2, which led to
            # calling 'found_face' AND then lost track of the face

            if y_level == 0:
                y_level = 1
                x_block = 1
                for y_val in range(20, -61, -5):
                    y_angle = y_val
                    print("LEVEL{0} - Y angle: {1}".format(y_level, -(y_angle)))
                    if y_level % 2 == 1:
                        for x_val in range(60, -61, -2):
                            x_angle = x_val
                            if x_block == 1:
                                tilt.set_angle(y_angle)
                            pan.set_angle(x_angle)
                            sleep(0.1)
                            print("   BLOCK{0}  ->>  X-angle: {1}".format(x_block, -(x_angle)))
                            if num_people.value == 1:
                                print("HUMAN FACE DETECTED AT LEVEL{0}, BLOCK{1}".format(y_level, x_block))
                                found_face(y_level)
                            if x_block < 61:
                                x_block += 1
                    elif y_level % 2 == 0:
                        for x_val in range(-60, 61, 2):
                            x_angle = x_val
                            if x_block == 61:
                                tilt.set_angle(y_angle)
                            pan.set_angle(x_angle)
                            sleep(0.1)
                            print("   BLOCK{0}  ->>  X-angle: {1}".format(x_block, -(x_angle)))
                            if num_people.value == 1:
                                print("HUMAN FACE DETECTED AT LEVEL{0}, BLOCK{1}".format(y_level, x_block))
                                found_face(y_level)
                            if x_block > 1:
                                x_block -= 1
                    y_level += 1
            # ---------------------------------------------------------------------------------------
            # CASE2 - Losing track of a human face once detected at level > 2
            elif y_level != 0:
                y_levelAngle = 20 - ((y_level - 1) * 5)
                for y_val in range(y_levelAngle, -61, -5):
                    y_angle = y_val
                    print("LEVEL{0} - Y angle: {1}".format(y_level, -(y_angle)))
                    if y_level % 2 == 1:
                        x_block = 1
                        for x_val in range(60, -61, -2):
                            x_angle = x_val
                            if x_block == 1:
                                tilt.set_angle(y_angle)
                            pan.set_angle(x_angle)
                            sleep(0.1)
                            print("   BLOCK{0}  ->>  X-angle: {1}".format(x_block, -(x_angle)))
                            if num_people.value == 1:
                                print("HUMAN FACE DETECTED AT LEVEL{0}, BLOCK{1}".format(y_level, x_block))
                                found_face(y_level)
                            if x_block < 61:
                                x_block += 1
                    elif y_level % 2 == 0:
                        x_block = 61
                        for x_val in range(-60, 61, 2):
                            x_angle = x_val
                            if x_block == 61:
                                tilt.set_angle(y_angle)
                            pan.set_angle(x_angle)
                            sleep(0.1)
                            print("   BLOCK{0}  ->>  X-angle: {1}".format(x_block, -(x_angle)))
                            if num_people.value == 1:
                                print("HUMAN FACE DETECTED AT LEVEL{0}, BLOCK{1}".format(y_level, x_block))
                                found_face(y_level)
                            if x_block > 1:
                                x_block -= 1
                    y_level += 1

                if y_level > 17:
                    y_level = 0

    # 2nd method -->> found_face(int y_level)
    def found_face(y_level):
        print("HUMAN FACE DETECTED!!")
        sleep(3)
        step = 2

        # move_x(int step)
        def move_x(step):
            x_step = step
            if faceCoordinates[0] > 320:
                pan.set_angle(pan.get_angle() + x_step)
                sleep(0.3)
                # if faceCoordinates[0] < 320:
                    # print("Inside Face Coordinates < 320")
                    # print("Initial Pan Angle: {0}, Initial Face Coordinate: {1} ".format(pan.get_angle(), faceCoordinates[0]))
                    # x_step = ((640 / 120) * 2)
                    # pan.set_angle(pan.get_angle() - x_step)
                    # print("Post Pan Angle: {0}, Post Face Coordinate: {1} ".format(pan.get_angle(), faceCoordinates[0]))
                    # sleep(0.3)
            elif faceCoordinates[0] < 320:
                pan.set_angle(pan.get_angle() - x_step)
                sleep(0.3)
                # if faceCoordinates[0] > 320:
                    # print("Inside Face Coordinates > 320")
                    # print("Initial Pan Angle: {0}, Initial Face Coordinate: {1} ".format(pan.get_angle(), faceCoordinates[0]))
                    # x_step = ((640 / 120) * 2)
                    # pan.set_angle(pan.get_angle() + x_step)
                    # print("Post Pan Angle: {0}, Post Face Coordinate: {1} ".format(pan.get_angle(), faceCoordinates[0]))
                    # sleep(0.3)

        # move_y(int step)
        def move_y(step):
            y_step = step
            if faceCoordinates[1] > 240:
                tilt.set_angle(tilt.get_angle() + y_step)
                sleep(0.3)
                # if faceCoordinates[1] < 240:
                    # y_step = ((240 - faceCoordinates[1]) * 40) / 240
                    # tilt.set_angle(tilt.get_angle() - y_step)
                    # sleep(0.3)
            elif faceCoordinates[1] < 240:
                tilt.set_angle(tilt.get_angle() - y_step)
                sleep(0.3)
                # if faceCoordinates[1] > 240:
                    # y_step = ((faceCoordinates[1] - 240) * 40) / 240
                    # tilt.set_angle(tilt.get_angle() + y_step)
                    # sleep(0.3)

        while ((faceCoordinates[0] >= 330 or faceCoordinates[0] <= 310) or (faceCoordinates[1] >= 250 or faceCoordinates[1] <= 230)):
            move_x(step)
            move_y(step)
            sleep(1)
            if num_people.value != 1:
                sleep(3)
                if num_people.value != 1:
                    if y_level == 0 or y_level == 1 or y_level == 2:
                        searching(0, 0)
                    else:
                        searching(0, (y_level - 1))

    # start_servo() BODY
    x_block = 0
    y_level = 0
    if num_people.value == 1:
        found_face(y_level)
    else:
        searching(x_block, y_level)


import cv2
import os
from picamera2 import Picamera2, Preview
from libcamera import Transform


def headshot(name):
    image_counter = 0

    dataset_path = "/home/student/mcr4-version-3.0/User Database/dataset/" + name
    os.makedirs(dataset_path, exist_ok=True)

    picam2 = Picamera2()
    preview_config = picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)},
                                                         transform = Transform(vflip=1))
    capture_config = picam2.create_still_configuration(transform = Transform(vflip=1))
    picam2.configure(preview_config)
    picam2.start()

    while True:
        im = picam2.capture_array()

        cv2.imshow("Camera", im)
        k = cv2.waitKey(1)
        if k%256 == 27:  # ESC Pressed
            break
        elif k%256 == 32: # SPACE Pressed
            image_name = f"/home/student/mcr4-version-3.0/User Database/dataset/{name}/image{image_counter}.jpg"
            picam2.switch_mode_and_capture_file(capture_config, image_name)
            print(f"{image_name} written!")
            image_counter += 1
        
    cv2.destroyAllWindows()
    picam2.close()

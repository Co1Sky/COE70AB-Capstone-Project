import pigpio
import time

# Set the GPIO pin to use
led_pin = 17

# Connect to the pigpio daemon
pi = pigpio.pi()

# Check if the connection was successful
if not pi.connected:
    print("Failed to connect to pigpio daemon. Exiting.")
    exit()

try:
    while True:
        # Turn the LED on
        pi.write(led_pin, 1)
        
        # Wait for a second
        time.sleep(1)
        
        # Turn the LED off
        pi.write(led_pin, 0)
        
        # Wait for another second
        time.sleep(1)

except KeyboardInterrupt:
    # If the user interrupts the program, clean up GPIO settings
    pi.write(led_pin, 0)  # Turn off the LED
    pi.stop()


import cv2
import numpy as np
import RPi.GPIO as GPIO
import time

# Define the GPIO pin number to control the motor
MOTOR_PIN = 32  # just a general purpose pin

# Set up the GPIO pin
GPIO.setmode(GPIO.BOARD)  # mind the phycical pin position
GPIO.setup(MOTOR_PIN, GPIO.OUT)

# Initialize the camera
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

# Define the lower and upper bounds of the red color in HSV color space
lower_red = np.array([0, 50, 50])
upper_red = np.array([10, 255, 255])

while True:
    # Capture a frame from the camera
    ret, frame = camera.read()

    # Convert the frame to the HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a mask for the red color using the lower and upper bounds
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Find contours in the mask
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Check if any contours are detected
    if contours:
        # Start the motor if a red object is detected
        GPIO.output(MOTOR_PIN, GPIO.HIGH)
        print("Red object detected, stopping motor")
    else:
        # Stop the motor if no red object is detected
        GPIO.output(MOTOR_PIN, GPIO.LOW)

    # Display the mask on the screen
    cv2.imshow("Mask", mask)

    # Wait for a key press and exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and clean up the GPIO pin
camera.release()
GPIO.cleanup()
cv2.destroyAllWindows()
import cv2
import numpy as np
import RPi.GPIO as GPIO
import time
import speech_recognition as sr
import threading

other_codes = False  # refers to motor, ultrasonic and Pi camera

# we have CAMERA,MOTOR,ULTRA,VOICE
# Define the GPIO pin number to control the motor
# general purpose pin

# initalizing voice recognition
r = sr.Recognizer()
mic = sr.Microphone()
r.operation_timeout = 10

# motor pins
in1 = 24
in2 = 23
en = 25
temp1 = 1

# ultrasonic pins
GPIO_TRIGGER = 18
GPIO_ECHO = 17

# set motor
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(en, GPIO.OUT)
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
p = GPIO.PWM(en, 1000)
p.start(25)

# set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

# Initialize the camera
camera = cv2.VideoCapture(0)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

# Define the lower and upper bounds of the green color in HSV color space
lower_red = np.array([45, 100, 20])
upper_red = np.array([75, 255, 255])


# calculating distance by ultrasonic
def dist():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()
    # save StartTime

    while GPIO.input(GPIO_ECHO) == 0:
        continue

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, (the distance was doubled)
    distance = (TimeElapsed * 34300) / 2

    return distance


# setting the speech function
def speechrecognition():
    while True:
        try:
            with mic as source:
                audio = r.listen(source)

            words = r.recognize_google(audio)
            wordlist = words.split()
            print(wordlist)

            if "Mississippi" in wordlist:
                return wordlist  # returns a list of words with 'Mississippi' in it

        except:
            continue  # reloops when an error is detected in the function


# setting the camera function

def camera_read(camera):
    ret, frame = camera.read()
    # Convert the frame to the HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Create a mask for the red color using the lower and upper bounds
    mask = cv2.inRange(hsv, lower_red, upper_red)
    # Find contours in the mask
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # contours gives a boolean
    # Display the mask on the screen
    return contours


# calls the speechrecognition function
speech = speechrecognition()

# VOICE RECOGNITION STARTS AFTER 'mississippi'

if "Mississippi" in speech:
    other_codes = True

# EVERY OTHER CODE EXCEPT VOICE RECOGNITION will run next


while other_codes:
    distance = dist()  # returns the distance calculated by ultrasonic
    print("distance=", distance)

    caminfo = camera_read(camera)  # returns a None when no contours and a list when contours

    # combining ultrasonic and Picamera
    if distance >= 10 and caminfo:
        x = 'm'

    elif distance >= 50 and not caminfo:
        x = 'r'
    elif distance >= 35 and not caminfo:
        x = 'h'
    elif distance >= 10 and not caminfo:
        x = 'l'
    elif distance < 10:
        x = 's'

    # motor command by value of 'r'
    if x == 'r':
        print("run")
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
        p.ChangeDutyCycle(100)
        print("forward")
        x = 'z'


    elif x == 's':
        print("stop")
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.LOW)
        x = 'z'

    elif x == 'f':
        print("forward")
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
        temp1 = 1
        x = 'z'

    elif x == 'b':
        print("backward")
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.HIGH)
        p.ChangeDutyCycle(100)
        temp1 = 0
        x = 'z'

    elif x == 'l':
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
        print("low")
        p.ChangeDutyCycle(25)
        x = 'z'

    elif x == 'm':
        print("medium")
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
        p.ChangeDutyCycle(50)
        x = 'z'

    elif x == 'h':
        print("high")
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
        p.ChangeDutyCycle(75)
        x = 'z'


    elif x == 'e':
        GPIO.cleanup()
        break

    else:
        print("<<<  wrong data  >>>")
        print("please enter the defined data to continue.....")

# Release the camera and clean up the GPIO pin
camera.release()
GPIO.cleanup()
cv2.destroyAllWindows()
import RPi.GPIO as GPIO
import time

# Set up GPIO pins for ultrasonic sensor and motor control
GPIO.setmode(GPIO.BOARD)
trigger_pin = 11
echo_pin = 13
motor_pin = 12
GPIO.setup(trigger_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)
GPIO.setup(motor_pin, GPIO.OUT)

# Function to measure distance using ultrasonic sensor
def measure_distance():
    # Send a pulse to the ultrasonic sensor
    GPIO.output(trigger_pin, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trigger_pin, GPIO.LOW)

    # Measure the time it takes for the echo to return
    pulse_start = time.time()
    while GPIO.input(echo_pin) == 0:
        pulse_start = time.time()
    pulse_end = time.time()
    while GPIO.input(echo_pin) == 1:
        pulse_end = time.time()

    # Calculate distance based on the time it took for the echo to return
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    return distance

while True:
    # Measure distance to obstacle using ultrasonic sensor
    distance_to_obstacle = measure_distance()

    # If obstacle is less than 15 cm away, stop the motor
    if distance_to_obstacle < 15:
        GPIO.output(motor_pin, GPIO.LOW)
    else:
        GPIO.output(motor_pin, GPIO.HIGH)

    # Wait for a short amount of time before measuring distance again
    time.sleep(0.1)

# Clean up GPIO pins
GPIO.cleanup()

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
# motor pins by BCM
in1 = 24
in2 = 23
en = 25
temp1 = 1

# ultra pin by BCM
# set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 17

# set motor
# GPIO.setmode(GPIO.BCM)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(en, GPIO.OUT)
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
p = GPIO.PWM(en, 1000)
p.start(25)
# print("\n")
# print("The default speed & direction of motor is LOW & Forward.....")
# print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
# print("\n")

# set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)


def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()
    print(StartTime)
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
        # print("Start",StartTime)

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
        # print("Stop",StopTime)

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    # print(distance)

    return distance


# distance and command

if __name__ == '__main__':

    while (1):

        distance = distance()
        print("Measured Distance = %.1f cm" % distance)
        time.sleep(1)
        if distance >= 100:
            x = 'r'
        elif distance >= 60:
            x = 'b'
        elif distance < 15:
            x = 's'

            # x=input()
            # x=distance

            if x == 'r':
                print("run")
                if (temp1 == 1):
                    GPIO.output(in1, GPIO.HIGH)
                    GPIO.output(in2, GPIO.LOW)
                    p.ChangeDutyCycle(75)
                    print("forward")
                    x = 'z'
                else:
                    GPIO.output(in1, GPIO.LOW)
                    GPIO.output(in2, GPIO.HIGH)
                    print("backward")
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
                temp1 = 0
                x = 'z'

            elif x == 'l':
                print("low")
                p.ChangeDutyCycle(25)
                x = 'z'

            elif x == 'm':
                print("medium")
                p.ChangeDutyCycle(50)
                x = 'z'

            elif x == 'h':
                print("high")
                p.ChangeDutyCycle(75)
                x = 'z'


            elif x == 'e':
                GPIO.cleanup()
                break

            else:
                print("<<<  wrong data  >>>")
                print("please enter the defined data to continue.....")
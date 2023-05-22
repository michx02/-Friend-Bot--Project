# SLDP-Project

‘‘Friend Bot’’ used Python as the primary language for programming. Firstly, the required libraries were installed. These included RPi.GPIO and time library for the Ultrasonic sensor, cv2, NumPy for the Pi camera, and Google translate, threading, and speech recognition for the microphone to perform speech recognition. The motor driver module was connected to the Raspberry Pi's GPIO pins. The ultrasonic sensor was then programmed to measure the distance from the ‘Friend Bot’ to any obstacle in front of it. The camera Pi was set to produce contours when it detects a green object. The microphone was programmed to listen and start the entire program when it detected the word ‘Mississippi’ which is the pet name. The ‘Friend Bot’ stopped when it detected a distance of less than 10 cm, moved at low speed( motor power= 25) when the distance was less than 35cm but greater than 10cm, and accelerated (motor power= 100) when the distance was greater than 35cm. When contours were detected the ‘Friend Bot’ moved towards the contours at a medium speed( motor power= 50) and stopped when it was 10 cm away from the contours.

import RPi.GPIO as GPIO
import time
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 10
GPIO_ECHO = 12
GPIO_LED = 8
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_LED, GPIO.OUT)

# set GPIO17 as PWM, 100Hz freq
pwm = GPIO.PWM(GPIO_LED, 100)
# start at 0%
pwm.start(0)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, GPIO.HIGH)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, GPIO.LOW)
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = ((StopTime - StartTime) * 34300) / 2
 
    return distance
 

try:
    while True:
        # multiply distance by 3 to demonstrate LED brightness in smaller range of motion
        dist = distance() * 3
        # ensure distance stays within bounds of 0-100
        if dist < 0:
            dist = 0
        if dist > 100:
            dist = 100
        # set the brightness by subtracting the distance from the max brightness
        pwm.ChangeDutyCycle(100 - dist)
        time.sleep(0.1)
            
except KeyboardInterrupt:
    GPIO.cleanup()
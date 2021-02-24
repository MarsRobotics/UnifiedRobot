import sys
sys.path.insert(0, '/home/pi/Robotics/UnifiedRobot')
from lib import *

def servoTest():
    while True:
        angle = int(input())
        servo.setAngle(angle)

def DCTest():
    while True:
        try:
            speed = int(input())
            dc_motor.drive(speed)
        except Exception as e:
            print("Out of bounds. Enter a number from -100 to 100")
            print(e)


if __name__ == '__main__':
    test = input("Enter the test you would like to run:")
    if test == "servo":
        servo = Servo(18)
        servoTest()
    if test == "dc_brush":
        dc_motor = DCBrushed(128, 1)
        DCTest()

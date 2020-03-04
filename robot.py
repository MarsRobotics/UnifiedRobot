from lib.Servo import Servo
from lib.DCBrushed import DCBrushed


servoTest():
    while True:
        angle = int(input())
        servo.setAngle(angle)

DCTest():
    while True:
        speed = int(input())
        dc_motor.drive(speed)


if __name__ == '__main__':
    test = input("Enter the test you would like to run:")
    if test is "servo":
        servo = Servo(18)
        servoTest()
    if test is "dc_brush":
        dc_motor = DCBrushed(128, 1)
        DCTest()

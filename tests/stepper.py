import sys
sys.path.insert(0, '/home/pi/Robotics/UnifiedRobot')
from lib import Stepper

def stepperTest():
    while True:
        steps = int(input("Steps: "))
        delay = int(input("Delay: "))
        direction = int(input("Direction: "))
        stepper.step(steps, delay, direction)

if __name__ == '__main__':
    stepper = Stepper(18, 23, 24, 0.0005)
    stepperTest()

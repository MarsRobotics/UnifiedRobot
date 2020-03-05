import sys
sys.path.insert(0, '/home/pi/Robotics/UnifiedRobot')
from lib import Stepper

def stepperTest():
    while True:
        command = input("Command (s, e, d)")
        if command == "s":
            steps = int(input("Steps: "))
            delay = float(input("Delay: "))
            direction = int(input("Direction: "))
            stepper.step(steps, delay, direction)
        elif command == "e":
            stepper.enable()
        else:
            stepper.disable()

if __name__ == '__main__':
    stepper = Stepper.Stepper(24, 23, 18, 0.0005)
    stepperTest()

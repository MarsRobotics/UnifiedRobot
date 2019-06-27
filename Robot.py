from lib.RPi_Sabertooth import *

"""
    Class to act as an API for the robot to allow manual and autonomous control to be nicely modular. Most is ported from Arduino code.
"""
class Robot:
    def test():
        wheels = Sabertooth()
        for i in range(5):
            wheels.drive(address=i, speed=30, motor=0)
            wheels.drive(i, 30, 1)
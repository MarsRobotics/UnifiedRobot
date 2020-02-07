from pysabertooth import Sabertooth
import serial

"""
    Class to act as an API for the robot to allow manual and autonomous control to be nicely modular. Most is ported from Arduino code. The Arduino code can be found here: https://github.com/MarsRobotics/Arduino-Code/blob/master/Arduino_Code/Arduino_Code.ino
"""

saber = Sabertooth('/dev/serial0', baudrate=9600, address=128)
saber.drive(1, 50)
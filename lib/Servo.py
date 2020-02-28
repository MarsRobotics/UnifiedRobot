from RpiMotorLib import rpi_pservo_lib

class Servo:

    def __init__(self, pin, pwm_min_width, pwn_max_width):
        self.pin = pin
        self.motor = rpi_pservo_lib.ServoPigpio(y_one=pwm_min_width, y_two=pwn_max_width)
        self.angle = None
        self.verbose = False
    
    def setAngle(self, degree):
        pwm = self.motor.convert_from_degree(degree)
        self.motor.servo_move(self.pin, pwm, verbose=self.verbose)
        self.angle = degree

    def setVerbose(self, isVerbose):
        self.verbose = isVerbose
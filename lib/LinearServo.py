from RpiMotorLib import rpi_pservo_lib

class LinearServo:

    def __init__(self, pin, pwm_extend=1000, pwm_retract=2000):
        """
        A servo motor class. This is not intended for continuous servo motors.

        Dependencies: 
            RpiMotorLib (https://github.com/gavinlyonsrepo/RpiMotorLib)

        Instance variables:
            pin = pin number of the raspberry pi that this motor is connected to
            pwm_min_width = "pulse width min in uS of servo % for 0 degrees"
            pwn_max_width = "pulse width max in uS of servo % for 180 degrees"
            verbose = boolean for printing a verbose 
        """
        self.pin = pin
        self.motor = rpi_pservo_lib.ServoPigpio(y_one=pwm_extend, y_two=pwm_retract)
        self.angle = None
        self.verbose = False
    
    def setAngle(self, degree):
        pwm = self.motor.convert_from_degree(degree)
        self.motor.servo_move(self.pin, pwm, verbose=self.verbose)
        self.angle = degree

import pigpio
from time import sleep

class Stepper:

    def __init__(self, dis_pin, dir_pin, step_pin, default_delay):
        """
        A stepper motor class originally made for the Geckodrive G213V
            
        Dependencies:
            pigpio

        Instance Variables:
            pi: The pigpio instance of the RPi's gpio pins
            dis_pin: The pin for disabling the stepper
            dir_pin: Pin for setting the turning direction of the stepper
            step_pin: Pin for stepping the motor
            position: the number of steps the stepper has gone from its initial state
            default_delay: the initial delay to run the stepper at (will ramp up to the speed if the delay is smaller than the default)
        """
        self.pi = pigpio.pi()
        self.dis_pin = dis_pin
        self.dir_pin = dir_pin
        self.step_pin = step_pin
        self.default_delay = default_delay
        self.pi.set_mode(dis_pin, pigpio.OUTPUT)
        self.pi.set_mode(dir_pin, pigpio.OUTPUT)
        self.pi.set_mode(step_pin, pigpio.OUTPUT)
        self.position = 0
        self.disable()#default the stepper to being powered off

    def enable(self):
        self.pi.write(dis_pin, 0)#holds position of the stepper

    def disable(self):
        self.pi.write(dis_pin, 1)#disable the stepper. Let's it move freely, but does not take power

    def step(self, step_count, delay=self.default_delay, direction=0):
        self.enable()
        self.pi.write(dir_pin, direction)
        count = 0
        my_delay = self.default_delay
        while count < step_count:
            self.pi.write(step_pin, 1)
            sleep(my_delay)
            self.pi.write(step_pin, 0)
            sleep(my_delay)
            count += 1
        self.disable()

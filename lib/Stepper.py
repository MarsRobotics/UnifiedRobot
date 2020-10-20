import pigpio
from time import sleep

class Stepper:

    def __init__(self, disable_pin, dir_pin, step_pin, pi, steps_per_rev=400, revs_per_turn=60, default_delay=0.0005):
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
        self.steps_per_turn = steps_per_rev*revs_per_turn #How many steps the motor must turn to turn the output device one full revolution
        self.angle = 0

        self.pi = pi
        self.dis_pin = disable_pin
        self.dir_pin = dir_pin
        self.step_pin = step_pin
        self.default_delay = default_delay
        self.pi.set_mode(disable_pin, pigpio.OUTPUT)
        self.pi.set_mode(dir_pin, pigpio.OUTPUT)
        self.pi.set_mode(step_pin, pigpio.OUTPUT)
        self.position = 0
        self.disable()#default the stepper to being powered off

    def enable(self):
        self.pi.write(self.dis_pin, 0)#holds position of the stepper

    def disable(self):
        self.pi.write(self.dis_pin, 1)#disable the stepper. Let's it move freely, but does not take power

    def setAngle(self, angle):
        step_count = self.steps_per_turn * (self.angle - angle) / 360
        print(step_count)
        self.step(int(step_count), self.default_delay)

    def step(self, step_count, delay, direction=0):
        #enable the motor and set the direction
        self.enable()
        if step_count < 0:
            direction = 0 if direction == 1 else 1
            step_count = abs(step_count)
        self.pi.write(self.dir_pin, direction)
        sleep(1)
        
        my_delay = max(delay, self.default_delay)

        #step the motor and ramp the initial delay to the passed delay
        for i in range(step_count):
            if my_delay > delay:
                my_delay -= 0.000001
            self.pi.write(self.step_pin, 1)
            sleep(my_delay)
            self.pi.write(self.step_pin, 0)
            sleep(my_delay)
            self.position += 1 if (direction == 0) else -1
        self.disable()

import pigpio
from time import sleep

class Stepper:

    def __init__(self, disable_pin, dir_pin, step_pin, pi, steps_per_rev=200, revs_per_turn=60, delay=0.15):
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
            delay: the smallest delay achievable by the motor. Will not allow a delay smaller than this
        """
        self.steps_per_turn = steps_per_rev*revs_per_turn #How many steps the motor must turn to turn the output device one full revolution
        self.curr_angle = 0
        self.step_count = 0
        self.position = 0
        self.direction = 0
        self.running = False

        self.pi = pi
        self.dis_pin = disable_pin
        self.dir_pin = dir_pin
        self.step_pin = step_pin
        self.delay= delay
        try:
            self.pi.set_mode(disable_pin, pigpio.OUTPUT)
        except Exception as e:
            print('Disable pin failure')
        try:
            self.pi.set_mode(dir_pin, pigpio.OUTPUT)
        except Exception as e:
            print('Direction pin failure')
        try:
            self.pi.set_mode(step_pin, pigpio.OUTPUT)
        except Exception as e:
            print('Step pin failure')

        self.position = 0
        self.disable()#default the stepper to being powered off

    def enable(self):
        self.pi.write(self.dis_pin, 0)#holds position of the stepper

    def disable(self):
        self.pi.write(self.dis_pin, 1)#disable the stepper. Let's it move freely, but does not take power

    def setAngle(self, angle):
        self.curr_angle = self.position * 360 / self.steps_per_turn
        self.step_count = self.steps_per_turn * (self.curr_angle - angle) / 360
        self.direction = 0 if self.step_count > 0 else 1
        self.pi.write(self.dir_pin, self.direction)
        self.running = True
        self.enable()

    def step(self):
        if self.step_count == 0:
            self.disable()
            self.running = False
            return
        self.pi.write(self.step_pin, 1)
        sleep(delay/1000)
        self.pi.write(self.step_pin, 0)
        self.position += 1 if (self.direction == 0) else -1

    def getAngle(self):
        self.curr_angle = self.position * 360 / self.steps_per_turn
        return self.curr_angle

    def isRunning(self):
        return self.running

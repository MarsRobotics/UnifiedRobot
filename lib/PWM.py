import RPi.GPIO as GPIO

class PWM:

    MIN_RANGE = 0
    MAX_RANGE = 100

    def __init__(self, pin, freq, min_dc, max_dc, init_range, invert=False):
        """
        A PWM class that sets RPi pin to specified duty cycle and freqency
            
        Dependencies:
            RPi.GPIO
        Parameters:
            pin: Board pin of signal (BCM)
            min_dc: Maximum duty cycle of motor (%)
            max_dc: Minimum duty cycle of motor (%)
            init_range: Initial % of the duty cycle range (%)
                        0 = min_dc, 100 = max_dc
            freq: frequency of PWM (hz)
            invert: reverses PWM range mapping
        """
        if (init_range < self.MIN_RANGE or init_range > self.MAX_RANGE):
            raise ValueError("init DC is not between min and max dc")
        self.min_dc = min_dc
        self.max_dc = max_dc
        self.init_range = init_range
        self.invert = invert
        try:
            GPIO.setmode(GPIO.BCM)
        except Exception as e:
            print('GPIO failure')
        try:
            GPIO.setup(pin, GPIO.OUT, initial = GPIO.LOW)
        except Exception as e:
            print('Pin setup failure')

        self.pwm = GPIO.PWM(pin, freq)
        self.pwm.start(self.convertRangeToDutyCycle(init_range))

    def convertRangeToDutyCycle(self, percent):
        if (percent < self.MIN_RANGE or percent > self.MAX_RANGE):
            print('Servo set out of bounds')
            percent = self.init_range
        dc = (percent * (self.max_dc - self.min_dc) / self.MAX_RANGE) + self.min_dc
        return self.max_dc + self.min_dc - dc if (self.invert) else (dc)
        
    def setPosition(self, percent):
        self.pwm.ChangeDutyCycle(self.convertRangeToDutyCycle(percent))

    def disable(self):
        # TODO: Doesn't disable if turning. Maybe try setting frequency to 0?
        self.pwm.ChangeDutyCycle(0)

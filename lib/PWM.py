import RPi.GPIO as GPIO

class PWM:

    def __init__(self, pin, freq, min_dc, max_dc, init_dc, invert=False):
        """
        A PWM class that sets RPi pin to specified duty cycle and freqency
            
        Dependencies:
            RPi.GPIO
        Parameters:
            pin: Board pin of signal (BCM)
            min_dc: Maximum duty cycle of motor (%)
            max_dc: Minimum duty cycle of motor (%)
            init_dc: Initial duty cycle of motor (%)
            freq: frequency of PWM (hz)
            invert: reverses PWM range mapping
        """
        if (init_dc < min_dc or init_dc > max_dc):
            raise ValueError("init DC is not between min and max dc")
        self.min_dc = min_dc
        self.max_dc = max_dc
        self.init_dc = init_dc
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
        self.pwm.start(convertDutyCycle(init_dc))

    def convertDutyCycle(self, dc):
        if (dc < 0 or dc > 100):
            print('Servo set out of bounds')
            dc = self.init_dc
        dc = (dc * (self.max_dc - self.min_dc) / 100) + self.min_dc
        return self.max_dc - dc if (self.invert) else (dc)
        
    def setDutyCycle(self, dc):
        self.pwm.ChangeDutyCycle(self.convertDutyCycle(dc))

    def disable(self):
        self.pwm.ChangeDutyCycle(0)

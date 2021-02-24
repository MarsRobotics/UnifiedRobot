from pysabertooth import Sabertooth

class DCBrushed:

    def __init__(self, address, motor_num):
        """
        A DC brushed motor class for sabertooth motor controllers in packetized serial
        
        Dependencies: 
            pysabertooth (https://github.com/MomsFriendlyRobotCompany/pysabertooth)

        Instance variables:
            address = address of the sabertooth motor controller in packetized serial mode 
            motor_num = 1 or 2; the port number of the motor controller of the sabertooth;
                        there are two motors available for each controller
        """
        self.address = address
        self.motor_num = motor_num
        self.motor = Sabertooth('/dev/serial0', baudrate=9600, address=self.address)
        
    def drive(self, speed):
        """
        Sets the motor to a given power

        speed = a value in the range [-100, 100]
        """
        self.motor.drive(self.motor_num, speed)
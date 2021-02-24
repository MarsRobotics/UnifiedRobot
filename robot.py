from lib.Servo import Servo
from lib.DCBrushed import DCBrushed
from lib.TrinamicsMotor import TrinamicsMotor
from lib.Stepper import Stepper
from time import sleep
import pigpio

class Robot:
    def __init__(self):
        self.drive_motors = []
        self.drive_speed = 2000#velocity of the drive motors in rpms
        can_host_id = 2
        min_can_id = 1
        max_can_id = 7
        self.art_motors = []
        pi = pigpio.pi()
        art_disable_pins = [[2,2,2], [2,2,2]] #TODO consider tying all these to one pin... Do we ever need to enable individual articulation motors?
        art_dir_pins = [[3,4,5], [17,18,19]]
        art_step_pins = [[6,12,13], [20,21,22]]
        for i in range(min_can_id, max_can_id):
            if i == can_host_id:
                continue
            try:
                self.drive_motors.append(TrinamicsMotor(i))#Initialize Trinamic Motors for drive
            except Exception as e:
                print(e)
                continue
            print("Motor found at ID {num:}.".format(num = i))
        for i in range(2):
            for j in range(3):
                try:
                    self.art_motors.append(Stepper(art_disable_pins[i][j], art_dir_pins[i][j], art_step_pins[i][j], pi, 200, 1))#Initialize stepper motors for articulation
                except Exception as e:
                    continue
        #TODO add DC Brushed motors as needed

        self.art_angles = [[0,0,0],[180,180,180],[135,180,135]]
        #TODO Add reading/writing the state of the robot from/to a file? Most importantly, save the a-joint angles.

    def articulate(self, angles):
        #TODO Unlock the solenoid pin
        for i in range(2):
            for j in range(3):
                self.art_motors[j+i*3].setAngle(angles[j])
                #TODO Make this non-blocking... Start on a thread that will callback?
                #TODO Make the drive motors run at the correct speed as well
        #TODO Lock the solenoid pin
            

    def driveForward(self):
        self.articulate(self.art_angles[1])
        for motor in self.drive_motors:
            motor.setVelocity(self.drive_speed)#Note that this is already non-blocking but will need to be disabled. I would recommend calling setTorque()
    
    def stop(self):
        for motor in self.drive_motors:
            motor.setTorque()#When setting the velocity to 0, the motors will power to stay at velocity 0.
            #calling setTorque() tells the motor to not allow any current to be drawn thus disabling the motor.
        #Articulation motors are steppers which must be manually driven, so there is no need to stop them manually.
        #TODO Stop the other motors once they are added
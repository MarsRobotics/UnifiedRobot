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

def servoTest():
    while True:
        angle = int(input())
        servo.setAngle(angle)

def DCTest():
    while True:
        speed = int(input())
        dc_motor.drive(speed)

def TrinamicTest():
    motors = []
    print("Checking for motors on IDs 1-6")
    for i in range(1, 7):
        if i == 2:
            continue
        try:
            motors.append(TrinamicsMotor(i))
        except:
            continue
        print("Motor found at ID {num:}.".format(num = i))
    print("Valid command are V(elocity) T(orque) P(osition) S(upply Voltage)")
    print("Supply Voltage can only be read")
    print("Setting Torque will set torque to 0 regardless of value for safety reasons")
    while True:
        command = input("Enter a command (ID R/W CMD VAL):")
        try:
            [num, rw, cmd, val] = command.split()
        except:
            try:
                [num, rw, cmd] = command.split()
            except:
                print("Improper command format.")
                continue
        m = None
        num = int(num)
        for motor in motors:
            if motor.getID() == num:
                m = motor
        if m is None:
            print("Motor ID not found.")
            continue
        if rw == "R":
            if cmd == "V":
                print(m.getVelocity())
            if cmd == "T":
                print(m.getTorque())
            if cmd == "S":
                v = m.getVoltage()
                if v < 21:
                    print("LOW VOLTAGE")
                print(v)
            if cmd == "P":
                print(m.getPosition())
        else:
            if cmd == "V":
                m.setVelocity(val)
                print("Velocity set")
            if cmd == "P":
                m.setPosition(val)
                print("Position set")
            if cmd == "T":
                m.setTorque()
                print("Driver off")

if __name__ == '__main__':
    robot = Robot()
    robot.driveForward()
    sleep(5)
    '''test = input("Enter the test you would like to run:")
    if test == "servo":
        servo = Servo(18)
        servoTest()
    if test == "dc_brush":
        dc_motor = DCBrushed(128, 1)
        DCTest()
    if test == "tri":
        TrinamicTest()'''

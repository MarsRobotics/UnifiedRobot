from lib.Servo import Servo
from lib.DCBrushed import DCBrushed
from lib.TrinamicsMotor import TrinamicsMotor

def servoTest():
    while True:
        angle = int(input())
        servo.setAngle(angle)

def DCTest():
    while True:
        speed = int(input())
        dc_motor.drive(speed)

def TrinamicTest():
    test = input("Enter the ID of the motor you would like to connect")
    motors = []
    while test is not "X":
        motors.append(TrinamicsMotor(test))
        test = input("Enter the next ID (or X to continue)")
    print("Valid command are V(elocity) T(orque) P(osition) S(upply Voltage)")
    print("Supply Voltage can only be read")
    print("Setting Torque will set torque to 0 regardless of value for safety reasons")
    while True:
        cmd = input("Enter a command (ID R/W CMD VAL):")
        [num, rw, cmd, val] = cmd.split()
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
                print(m.getVoltage())
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
    test = input("Enter the test you would like to run:")
    if test == "servo":
        servo = Servo(18)
        servoTest()
    if test == "dc_brush":
        dc_motor = DCBrushed(128, 1)
        DCTest()
    if test == "tri":
        TrinamicTest()

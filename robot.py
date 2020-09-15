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
    test = input("Enter the test you would like to run:")
    if test == "servo":
        servo = Servo(18)
        servoTest()
    if test == "dc_brush":
        dc_motor = DCBrushed(128, 1)
        DCTest()
    if test == "tri":
        TrinamicTest()

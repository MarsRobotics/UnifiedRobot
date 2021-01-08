from lib.TrinamicsMotor import TrinamicsMotor
from lib.Stepper import Stepper
import pigpio
import rospy
from std_msgs.msg import Float64

class control_loop:
    def callback0(data):
        self.wheel_left = data
        self.wheel_update = True
    def callback1(data):
        self.wheel_right = data
        self.wheel_update = True
    def callback2(data):
        self.ankle_left = data
        self.ankle_update = True
    def callback3(data):
        self.ankle_right = data
        self.ankle_update = True

    def __init__(self):
        rospy.init_node('motor_driver')
        rospy.Subscriber("motors/wheel/l", callback0)
        rospy.Subscriber("motors/wheel/r", callback1)
        rospy.Subscriber("motors/ankle/l", callback2)
        rospy.Subscriber("motors/ankle/r", callback3)

        self.drive_motors = []
        self.drive_speed = 2000 #velocity of the drive motors in rpms
        can_host_id = 2 #CAN ID of self
        min_can_id = 1 #First drive motor CAN ID
        max_can_id = 7 #Last drive motor CAN ID
        self.art_motors = []
        pi = pigpio.pi()
        # Pins for controlling the articulation steppers. Pin order is front to back, left to right. I.e. art_dir_pin[0][2] would be
        # the back left motor's direction pin.
        art_disable_pins = [[2,2,2], [2,2,2]]
        art_dir_pins = [[3,4,5], [17,18,19]]
        art_step_pins = [[6,12,13], [20,21,22]]
        for i in range(min_can_id, max_can_id): #Try to init all the drive motors
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
                    self.art_motors.append(Stepper(art_disable_pins[i][j], art_dir_pins[i][j], art_step_pins[i][j], pi))#Initialize stepper motors for articulation
                except Exception as e: #Most errors here are a result of pigpio errors... Typically they do not occur though fortunately.
                    continue
        #TODO add DC Brushed motors as needed

        self.art_hash = -1 # Hash of commands received from ROS. Let's us check if the command has been updated
        self.drive_hash = -1
        #TODO Add reading/writing the state of the robot from/to a file?
        self.run = True #Tells the control loop to keep running or not
        self.drive_run = False #Keeps track of whether or not the drive motors are running.
        self.drive_current = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]] #Tracks average drive motor current draw [running sum of draw, number of samples]
        self.wheel_left = []
        self.wheel_right = []
        self.wheel_update = False
        self.ankle_left = []
        self.ankle_right = []
        self.ankle_update = False

    def control(self):
        while self.run:
            # Articulation motor control
            if self.ankle_update: # If the angle is updated by ROS, update the Stepper angles
                for i in range(3):
                    self.art_motors[i].setAngle(int(self.ankle_left[i]))
                    self.art_motors[3+i].setAngle(int(self.ankle_right[i]) #Yeah indexing is funny...

            for m in self.art_motors:
                m.step()

            # Drive motor control
            if self.wheel_update: # node.speed will be the ROS node's drive speed. Will decide the units later...
                self.drive_run = True if self.speed != 0 else False
                for i in range(3):
                    self.drive_motors[i].setVelocityMS(float(self.wheel_right[i])) # This is in rpms. If self.speed is not in rpms, then do the appropriate conversions.
                    self.drive_motors[3+i].setVelocityMS(float(self.wheel_left[i]))

            # Drive motor torque (current) monitoring)
            if self.drive_run:
                for i in range(6):
                    c = self.drive_motors[i].getTorque() # Instantaneous current draw of drive motor
                    if self.drive_current[i][1] > 20: # Make sure we have enough samples to discern a trend... Adjust as needed
                        ave = self.drive_current[i][0] / self.drive_current[i][1] # Calculate average current draw
                        if c - ave > 1000: # Check for current spike. Adjust as needed
                            self.drive_motors[i].setTorque() # Disable stalling motor
                            continue # Don't add a stall sample to the average!
                    if self.drive_current[i][1] < 10000: # Get a large sample size but try to not overflow an int. Adjust as needed.
                        self.drive_current[i][0] += c
                        self.drive_current[i][1] += 1

            #TODO Excavation elevation control
            #TODO Excavation drive control
            #TODO Deposition control
            

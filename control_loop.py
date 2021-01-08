from lib.TrinamicsMotor import TrinamicsMotor
from lib.Stepper import Stepper
import pigpio

class control_loop:
    def __init__(self):
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

        self.art_angles = [[0,0,0],[180,180,180],[135,180,135]] #Packed, unpacked (drive forward/backward), turn left/right
        self.art_angle = 0 #0 = packed, 1 = unpacked, 2 = turn
        self.speed = 0 #Not sure how to best implement this
        #TODO Add reading/writing the state of the robot from/to a file?
        self.run = True #Tells the control loop to keep running or not
        self.drive_run = False #Keeps track of whether or not the drive motors are running.
        self.drive_current = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]] #Tracks average drive motor current draw [running sum of draw, number of samples]

    def control(self):
        while self.run:
            # Articulation motor control
            if node.art_angle != self.art_angle: # node.art_angle will be the ROS node's articulation angle mode
                self.art_angle = node.art_angle
                for i in range(2):
                    for j in range(3):
                        self.art_motors[3*i+j].setAngle(self.art_angles[self.art_angle][j]) #Yeah indexing is funny...
            for m in self.art_motors:
                m.step()

            # Drive motor control
            if node.speed != self.speed: # node.speed will be the ROS node's drive speed. Will decide the units later...
                self.speed = node.speed
                self.drive_run = True if self.speed != 0 else False
                for m in self.drive_motors:
                    m.setVelocity(self.speed) # This is in rpms. If self.speed is not in rpms, then do the appropriate conversions.

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
            

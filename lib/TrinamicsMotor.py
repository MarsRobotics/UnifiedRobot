import PyTrinamic
from PyTrinamic.connections.ConnectionManager import ConnectionManager
from PyTrinamic.modules.TMCM_1670 import TMCM_1670

class TrinamicsMotor:

    def __init__(self, motor_id=1, diameter=0.5, gear_ratio=60):
        self.m_per_sec_convert = 3.14159 * diameter / (gear_ratio * 60)
        self.rpm_convert = gear_ratio * 60 / (3.14159 * diameter)
        msg = "--interface socketcan_tmcl --host-id 2 --module-id {module}".format(module = motor_id)
        connectionManager = ConnectionManager(msg.split())
        self.myInterface = connectionManager.connect()

        self.motorID = motor_id
        self.module = TMCM_1670(self.myInterface)

        # motor configuration
        self.module.setMaxTorque(3000)
        #self.module.showMotorConfiguration()

        # encoder configuration
        #self.module.showEncoderConfiguration()

        # motion settings
        self.module.setMaxVelocity(4000)
        self.module.setAcceleration(4000)
        self.module.setRampEnabled(1)
        self.module.setTargetReachedVelocity(100)
        self.module.setTargetReachedDistance(1000)
        self.module.setMotorHaltedVelocity(5)
        #self.module.showMotionConfiguration()

        # PI configuration
        self.module.setTorquePParameter(2000) #4000 #2:000
        self.module.setTorqueIParameter(2000) #2000
        self.module.setVelocityPParameter(800) #1000
        self.module.setVelocityIParameter(600) #500
        self.module.setPositionPParameter(300)
        #self.module.showPIConfiguration()

        # use out_0 output for enable input (directly shortened)
        self.module.setDigitalOutput(0);

        # sync actual position with encoder N-Channel 
        self.module.setActualPosition(0)

    def __del__(self):
        try:
            self.setTorque()#Sets the target torque(current) to 0
        except:
            pass
        self.myInterface.close()

    def getID(self):
        return int(self.motorID)

    def getTorque(self):
        val = self.module.axisParameter(150)
        return val if val < 2147483647 else (val - 2147483647*2)

    def getPosition(self):
        val = self.module.axisParameter(1)
        return val if val < 2147483647 else (val - 2147483647*2)

    def getVelocity(self):
        val = self.module.axisParameter(3)
        return val if val < 2147483647 else (val - 2147483647*2)

    def getVoltage(self):
        return float(self.module.axisParameter(151))/10

    def setPosition(self, pos):
        self.module.setAxisParameter(0, int(pos))

    def setVelocity(self, vel):
        self.module.setAxisParameter(2, int(vel))

    def setVelocityMS(self, vel):
        speed = vel * self.rpm_convert
        self.module.setAxisParameter(2, int(vel))

    def setTorque(self):
        self.module.setAxisParameter(155, 0)

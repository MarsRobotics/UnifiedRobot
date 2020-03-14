import time
import PyTrinamic
from PyTrinamic.connections.ConnectionManager import ConnectionManager
from PyTrinamic.modules.TMCM_1670 import TMCM_1670

PyTrinamic.showInfo()
connectionManager = ConnectionManager("--interface socketcan_tmcl --host-id 2 --module-id 1".split())
myInterface = connectionManager.connect()

module = TMCM_1670(myInterface)

# motor configuration
module.setMaxTorque(3000)
module.showMotorConfiguration()

# encoder configuration
module.showEncoderConfiguration()

# motion settings
module.setMaxVelocity(4000)
module.setAcceleration(4000)
module.setRampEnabled(1)
module.setTargetReachedVelocity(100)
module.setTargetReachedDistance(1000)
module.setMotorHaltedVelocity(5)
module.showMotionConfiguration()

# PI configuration
module.setTorquePParameter(2000) #4000 #2:000
module.setTorqueIParameter(2000) #2000
module.setVelocityPParameter(800) #1000
module.setVelocityIParameter(600) #500
module.setPositionPParameter(300)
module.showPIConfiguration()

# use out_0 output for enable input (directly shortened)
module.setDigitalOutput(0);

# sync actual position with encoder N-Channel 
module.setActualPosition(0)

# move to first position
while True:
    vel = input()
    module.setAxisParameter(155, int(vel))
    #while True:
        #print("Current: " + str(module.axisParameter(150)))
        #time.sleep(0.5)

#module.moveToPosition(3000000)
#while not module.positionReached():
    #print("target position: " + str(module.targetPosition()) + " actual position: " + str(module.actualPosition()))
    #print("Current: " + str(module.axisParameter(150)))
    #time.sleep(0.2)
#print("Stage 1 Complete")
#module.moveToPosition(6000000)
#while not module.positionReached():
    #print("Current: " + str(module.axisParameter(150)))
    #print("target position: " + str(module.targetPosition()) + " actual position: " + str(module.actualPosition()))
    #time.sleep(0.2)

print("Ready.")
myInterface.close()
